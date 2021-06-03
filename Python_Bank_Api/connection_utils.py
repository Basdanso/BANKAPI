import os
from psycopg2._psycopg import OperationalError
from psycopg2 import connect


def create_connection():
    try:
        conn = connect(
            host=os.environ.get('HOST'),  # 'basdb.cljyge3jembp.us-east-2.rds.amazonaws.com',
            database=os.environ.get('DB_NAME'),  # 'postgres',
            user=os.environ.get('DB_USERNAME'),  # postgres',
            password=os.environ.get('DB_PASSWORD'),  # Bas12345',
            port=os.environ.get('PORT'),  # '5432'
        )
        return conn

    except OperationalError as e:

        print(e)


connection = create_connection()
