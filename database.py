import psycopg2
import logging

def get_db_connetion():
    try:
        con = psycopg2.connect(
            host="sua-db.postgres.database.azure.com",
            database="sua_db",
            user="postgres",
            password="p@ssw0rd",
            port=5432
        )
        return con
    except Exception as e:
        # print(f"Error connecting to database: {e}")
        logging.error(f"Error connecting to database: {e}")
        return None