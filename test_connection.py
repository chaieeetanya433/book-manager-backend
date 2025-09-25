# test_connection.py
import os
import psycopg2

try:
    conn = psycopg2.connect(
        host="db.qznjwzqijxhlwthhprwy.supabase.co",
        port=6543,  # Try pooler port
        database="postgres",
        user="postgres",
        password="4VvrdPW%88GU4_3",
        sslmode='require'
    )
    print("Connection successful!")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")