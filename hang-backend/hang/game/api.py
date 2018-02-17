from . import game
from .. import db
from ..models import Game, Guess, LibraryWord
from flask import jsonify, request

@game.route('/new', methods=['GET'])
def new():
    g = Game.start_new()
    response_obj = {
        'word_length': len(g.word),
        'game_code': g.code
    }
    return jsonify(response_obj), 200

@game.route('/<code>/check', methods=['POST'])
def check(code):
    if 'guess' not in request.get_json():
        return "Must pass letter in the request json", 400
    if Game.by_code(code) is None:
        return 'Game not found', 404
    if not Guess.is_valid(request.get_json()["guess"]):
        return "Must pass a single letter or number", 400
    if Guess.is_guess_on_game(request.get_json()["guess"], code):
        return "Cannot guess the same thing twice", 400
        
    guess_result = Game.by_code(code).check_guess(str(request.get_json()["guess"]))
    return jsonify(guess_result), 200

@game.route('/<code>/load', methods=['GET'])
def load(code):
    if Game.by_code(code) is None:
        return 'Game not found', 404

    return jsonify( Game.by_code(code).get_load_object() ), 200
    
@game.route('/challenge', methods=['POST'])
def challenge():
    if 'word' not in request.get_json():
        return 'We need a word to create a challenge.', 400
    if request.get_json()['word'] == "" :
        return 'We need a word to create a challenge.', 400
    if not LibraryWord.is_valid_word( request.get_json()['word'] ):
        return 'We can only make challenges of single alphanumeric words.', 400
    
    return Game.make_challenge_from_word(request.get_json()['word']), 200
    