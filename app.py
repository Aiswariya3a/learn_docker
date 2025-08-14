import time
from flask import Flask
import psycopg2

app = Flask(__name__)

def get_db_connection():
    # Connect to the database using the service name 'db' as the host.
    # The credentials match what we set in docker-compose.yml.
    while True:
        try:
            conn = psycopg2.connect(
                host="db",
                database="mydatabase",
                user="myuser",
                password="mypassword")
            return conn
        except psycopg2.OperationalError:
            print("Connection failed, retrying...")
            time.sleep(1)

@app.route('/')
def home():
    conn = get_db_connection()
    cur = conn.cursor()

    # Create a table if it doesn't exist
    cur.execute("CREATE TABLE IF NOT EXISTS visits (id serial PRIMARY KEY, timestamp timestamp);")
    # Insert the current time of the visit
    cur.execute("INSERT INTO visits (timestamp) VALUES (NOW());")
    conn.commit()

    # Get all visits to display
    cur.execute("SELECT timestamp FROM visits ORDER BY timestamp DESC;")
    visits = cur.fetchall()

    cur.close()
    conn.close()

    response = "<h1>Visitor Timestamps:</h1>"
    for visit in visits:
        response += f"<p>{visit[0]}</p>"

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)