# file: main.py
from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def home():
    # This sends a request to our api service.
    # The hostname 'api' matches the service name in docker-compose.yml.
    # The port '5001' matches the port our api.py is running on.
    try:
        response = requests.get('http://api:5001')
        message = response.text
    except requests.exceptions.ConnectionError as e:
        message = f"Error connecting to the API: {e}"
    
    return f'<h1>The API says: "{message}"</h1>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)