from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
# resources={
#     r"/api/*": {
#         "origins": "http://localhost:3000"
#     }
# }

db = SQLAlchemy()

@app.route('/', methods=['GET'])
def get_data():
    return jsonify({"message": "Hello world", "status": "success"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)