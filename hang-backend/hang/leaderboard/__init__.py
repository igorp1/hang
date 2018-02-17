from flask import Blueprint

leaderboard = Blueprint('leaderboard', __name__)

from . import api