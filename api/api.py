# file: api/api.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def get_message():
    # This service just returns a simple string.
    return "Hello from the API container!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)