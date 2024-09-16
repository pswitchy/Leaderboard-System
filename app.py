from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from app.auth import auth_bp
from app.leaderboard import leaderboard_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(leaderboard_bp, url_prefix='/leaderboard')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('submit_score')
def handle_score_submission(data):
    user_id = data['user_id']
    score = data['score']
    game = data['game']
    r.zadd(f'{game}_leaderboard', {user_id: score})
    top_players = r.zrevrange(f'{game}_leaderboard', 0, 9, withscores=True)
    emit('update_leaderboard', top_players, broadcast=True)
    # Notify users if they are overtaken
    for player, _ in top_players:
        if player.decode('utf-8') != user_id:
            socketio.emit('notification', {'message': f'You have been overtaken by {user_id} in {game}!'}, room=player.decode('utf-8'))

if __name__ == '__main__':
    socketio.run(app, debug=True)
