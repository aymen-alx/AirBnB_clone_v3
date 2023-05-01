#!/usr/bin/python3
""" Flask api """
from api.v1.views import app_views
from flask_cors import CORS
from flask import Flask, jsonify, make_response
from models import storage
import os


app = Flask(__name__)
app.url_map.strict_slashes = False
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_handler(self):
    """ handle teardown """
    storage.close()


@app.errorhandler(404)
def error_404(ex):
    """ 404 """
    return make_response(jsonify({'error': 'Not found'}), 404)


HOST = os.getenv('HBNB_API_HOST', '0.0.0.0')
PORT = os.getenv('HBNB_API_PORT', '5000')

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, threaded=True)
