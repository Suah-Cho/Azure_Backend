import psycopg2

def getCon():
    con = psycopg2.connect(
        host="sua-db.postgres.database.azure.com",
        database="postgres",
        user="postgres",
        password="p@ssw0rd",
        port=5432
    )