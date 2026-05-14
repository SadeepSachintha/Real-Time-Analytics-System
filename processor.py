from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, avg, window, min, max
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

import os

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("SriLankanMarketAnalytics") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .getOrCreate()

KAFKA_HOST = os.getenv("KAFKA_HOST", "localhost")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")

# Schema for the incoming JSON data
schema = StructType([
    StructField("timestamp", StringType()),
    StructField("item_name", StringType()),
    StructField("unit", StringType()),
    StructField("price", DoubleType()),
    StructField("market", StringType()),
    StructField("region", StringType())
])

# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", f"{KAFKA_HOST}:29092" if KAFKA_HOST == "localhost" else f"{KAFKA_HOST}:9092") \
    .option("subscribe", "market-prices") \
    .option("startingOffsets", "latest") \
    .load()

# Parse JSON and Convert Timestamp
parsed_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*") \
    .withColumn("timestamp", col("timestamp").cast(TimestampType()))

# Perform Aggregations (Windowed: 30 seconds)
aggregated_df = parsed_df \
    .withWatermark("timestamp", "1 minute") \
    .groupBy(
        window(col("timestamp"), "30 seconds"),
        col("item_name")
    ) \
    .agg(
        avg("price").alias("avg_price"),
        min("price").alias("min_price"),
        max("price").alias("max_price")
    ) \
    .select(
        col("item_name"),
        col("avg_price"),
        col("min_price"),
        col("max_price"),
        col("window.end").alias("last_updated")
    )

# Function to write to PostgreSQL
def write_to_postgres(batch_df, batch_id):
    batch_df.write \
        .format("jdbc") \
        .option("url", f"jdbc:postgresql://{POSTGRES_HOST}:5432/analytics_db") \
        .option("dbtable", "processed_market_data") \
        .option("user", "admin") \
        .option("password", "adminpassword") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

# Start the Streaming Query
query = aggregated_df.writeStream \
    .foreachBatch(write_to_postgres) \
    .outputMode("update") \
    .start()

print("Real-Time Processor Started. Waiting for data...")
query.awaitTermination()
