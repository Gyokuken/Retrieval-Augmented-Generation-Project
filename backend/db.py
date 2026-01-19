import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()  # 🔑 THIS IS CRITICAL

def get_conn():
    host = os.getenv("SUPABASE_DB_HOST")
    port = os.getenv("SUPABASE_DB_PORT")
    db = os.getenv("SUPABASE_DB_NAME")
    user = os.getenv("SUPABASE_DB_USER")
    password = os.getenv("SUPABASE_DB_PASSWORD")
    print("DB HOST USED:", host)
    if not host:
        raise RuntimeError("SUPABASE_DB_HOST is not set")
    


    return psycopg2.connect(
        host=host,
        port=port,
        dbname=db,
        user=user,
        password=password,
        sslmode="require"
    )
    

