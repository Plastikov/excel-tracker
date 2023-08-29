from flask import Flask, request, jsonify
from src.views import mail

from src.views import views
from src.config.config import config
from src.models import db, migrate

def create_app(development='development'):
    app = Flask(__name__)
    
    app.config.from_object(config['development'])
    config['development'].init_app(app)
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app)
    
    
    app.register_blueprint(views)
    
    
    return app