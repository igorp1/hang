import uuid
from hang import db

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(45), unique=True, nullable=False)
    created_by = db.Column(db.String(45), nullable=True)

    def __init__(self, word, created_by=None):
        self.word = word
        self.created_by = created_by

    @staticmethod
    def is_valid_word(word):
        # not re.match('^[A-Za-z]+$', word)
        return True
    

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(6))
    word = db.Column(db.String(45), unique=True, nullable=False)
    db.Column(db.String(45), unique=True, nullable=False)
    guesses = db.relationship('Guess', backref="game", lazy="dynamic")

    def __init__(self, word, created_by=None):
        self.code = uuid.uuid4().hex[:6]
        self.word = word

class Guess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    letter = db.Column(db.String(1), nullable=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False )



