from flask import Flask
from api.api import api_blueprint
from db import db
from config import Config
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)    
    CORS(app)
    app.config['SECRET_KEY'] = 'your_secret_key_here' # THIS SHOULD NEVER BE HARD CODED INSIDE THE APPLICATION !
    db.init_app(app)    
    app.register_blueprint(api_blueprint, url_prefix="/api")    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)