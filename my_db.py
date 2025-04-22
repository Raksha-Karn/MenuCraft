import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

try:
    connection = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )

    cursor = connection.cursor()

    cursor.execute("SELECT version();")

    db_version = cursor.fetchone()
    cursor.close()
    connection.close()
    print("Database version:", db_version[0])

except Exception as error:
    print("Error while connecting to PostgreSQL:", error)
