import psycopg2
from psycopg2 import sql

def setup_database():
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
    except Exception as e:
        print(f"Error setting up database: {e}")

if __name__ == "__main__":
    setup_database()
