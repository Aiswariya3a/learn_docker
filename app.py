from flask import Flask
import psycopg2
import time

app = Flask(__name__)

@app.route('/')
def home():
    # Let's try to connect to the database
    try:
        conn = psycopg2.connect(
            host="db",
            database="mydatabase",
            user="myuser",
            password="mypassword"
        )
        # If we get here, the connection was successful!
        conn.close() # Close the connection right away
        return "<h1>Success! I connected to the database.</h1>"

    except psycopg2.OperationalError as e:
        # If we get here, something went wrong
        return f"<h1>Error: Could not connect. Is the database running?</h1><p>{e}</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)