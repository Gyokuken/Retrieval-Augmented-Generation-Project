import psycopg2

conn = psycopg2.connect(
    host="aws-1-ap-southeast-1.pooler.supabase.com",
    port=5432,
    dbname="postgres",
    user="postgres.iwavamvjeubhascgoyny",
    password="Amitanshulal",
)

cur = conn.cursor()
cur.execute("select 1;")
print("✅ Connected via Supabase pooler")
