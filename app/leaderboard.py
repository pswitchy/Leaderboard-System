from flask import Blueprint, request, jsonify
import redis
from .auth import token_required
import datetime

leaderboard_bp = Blueprint('leaderboard', __name__)
r = redis.Redis(host='redis', port=6379, db=0)

@leaderboard_bp.route('/submit-score', methods=['POST'])
@token_required
def submit_score():
    data = request.get_json()
    user_id = request.user
    score = data['score']
    game = data['game']
    timestamp = datetime.datetime.utcnow().isoformat()
    r.zadd(f'{game}_leaderboard', {user_id: score})
    r.lpush(f'{user_id}:{game}:history', f'{timestamp}:{score}')
    return jsonify({'message': 'Score submitted successfully!'})

@leaderboard_bp.route('/leaderboard/<game>', methods=['GET'])
def get_leaderboard(game):
    top_players = r.zrevrange(f'{game}_leaderboard', 0, 9, withscores=True)
    leaderboard = [{'user': user.decode('utf-8'), 'score': score} for user, score in top_players]
    return jsonify(leaderboard)

@leaderboard_bp.route('/score-history/<game>', methods=['GET'])
@token_required
def get_score_history(game):
    user_id = request.user
    history = r.lrange(f'{user_id}:{game}:history', 0, -1)
    history = [entry.decode('utf-8').split(':') for entry in history]
    return jsonify(history)
