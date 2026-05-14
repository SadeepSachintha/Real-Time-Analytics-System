import psycopg2
from psycopg2 import sql
import time

def setup_database():
    retries = 10
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="analytics_db",
                user="admin",
                password="adminpassword"
            )
            cur = conn.cursor()
            
            # Create table for processed market data
            create_table_query = """
            CREATE TABLE IF NOT EXISTS processed_market_data (
                id SERIAL PRIMARY KEY,
                item_name VARCHAR(50),
                avg_price DECIMAL(10, 2),
                min_price DECIMAL(10, 2),
                max_price DECIMAL(10, 2),
                last_updated TIMESTAMP
            );
            """
            cur.execute(create_table_query)
            conn.commit()
            print("Database table 'processed_market_data' created successfully.")
            
            cur.close()
            conn.close()
            return # Success
        except Exception as e:
            print(f"Waiting for database... ({retries} retries left) - {e}")
            retries -= 1
            time.sleep(5)
    
    print("Could not connect to database after several retries.")

if __name__ == "__main__":
    setup_database()
