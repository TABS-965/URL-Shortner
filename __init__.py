from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Ensure the instance directory exists
    instance_dir = os.path.dirname(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
    
    db.init_app(app)
    
    with app.app_context():
        from . import models
        db.create_all()  
        
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    return app