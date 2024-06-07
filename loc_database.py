import psycopg2 #type: ignore
from sshtunnel import SSHTunnelForwarder #type: ignore

def getCon():
    try:
        tunnel = SSHTunnelForwarder(
            ('40.82.144.200', 22),
            ssh_username='azureuser',
            ssh_pkey='~/.ssh/sua-vm_key.pem',
            remote_bind_address=('sua-db.postgres.database.azure.com', 5432)
        )

        tunnel.start()

        con = psycopg2.connect(
            host='localhost',
            port=tunnel.local_bind_port,
            user='postgres',
            password='p@ssw0rd',
            dbname='postgres'
        )

        return con
    except Exception as e:
        # logging.error(f"Error connecting to database: {e}")
        print("Error connecting to database: {e}")