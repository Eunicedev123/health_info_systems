import os
from flask import Flask
from config import config
from models import init_db
from routes.web import web
from routes.api import api

def create_app(config_name='default'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    app.register_blueprint(web)
    app.register_blueprint(api)
    
    return app

if __name__ == '__main__':
    # Get environment from system or use default
    env = os.environ.get('FLASK_ENV', 'development')
    app = create_app(env)
    app.run(host='0.0.0.0', port=5000)