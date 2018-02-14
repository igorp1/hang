from . import game
from .. import db
from ..models import Game

import re

@game.route('/start', methods=['GET'])
def game_start():
    return "Game started"


@game.route('/check', methods=['POST'])
def game_check():
    if not request.form["letter"]:
        return "Must pass letter in the request form", 400
    if not re.match("^[a-zA-Z]{1}$", request.form["letter"]):
        return "Must pass a single letter", 400
    return "Letter ({0}) found ".format(request.form["letter"])

