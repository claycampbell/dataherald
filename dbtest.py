import psycopg2

def test_connection():
    cursor = None
    connection = None
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            host="hakkoda.postgres.database.azure.com",
            port="5432",
            user="hakkoda",
            password="P@ssw0rd",
            dbname="postgres"
        )

        # Create a cursor object using the connection
        cursor = connection.cursor()
        
        # Execute a simple query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"Connected to - {version[0]}")
        
    except Exception as error:
        print(f"Error while connecting to PostgreSQL: {error}")
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("PostgreSQL connection closed.")

if __name__ == "__main__":
    test_connection()
