from . import leaderboard
from .. import db
from ..models import Score, Game
from flask import jsonify, request

@leaderboard.route('/save', methods=['POST'])
def save():
    if 'game' not in request.get_json():
        return "Must pass game in the request json", 400
    if 'player' not in request.get_json():
        return "Must pass letter in the request json", 400
    g_code = request.get_json()['game']
    player = request.get_json()['player']
    db.session.add( Score(player, Game.by_code(g_code)) )
    db.session.commit()
    return 'OK', 200

@leaderboard.route('/load', methods=['GET'])
def load():
    return jsonify( Score.get_top() ), 200