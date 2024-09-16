from flask import Flask
from flask_socketio import SocketIO
from .auth import auth_bp
from .leaderboard import leaderboard_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    
    # Initialize SocketIO
    socketio = SocketIO(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(leaderboard_bp, url_prefix='/leaderboard')
    
    return app, socketio
