from flask import Flask
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# TODO: import gemini api and use it for a request, figure out how to do files

@app.route('/')

def home():
    return "Hi"

if __name__ == '__main__':
    app.run(debug=True)