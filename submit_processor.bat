@echo off
echo Submitting Spark Job to Docker container...

docker exec -i -u root ^
  -e KAFKA_HOST=kafka ^
  -e POSTGRES_HOST=postgres ^
  spark-master spark-submit ^
  --master spark://spark-master:7077 ^
  --conf "spark.driver.extraJavaOptions=-Divy.home=/tmp/.ivy2" ^
  --conf "spark.executor.extraJavaOptions=-Divy.home=/tmp/.ivy2" ^
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.postgresql:postgresql:42.7.2 ^
  /opt/bitnami/spark/app/processor.py
