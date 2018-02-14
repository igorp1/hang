import uuid, re
from hang import db
from  sqlalchemy.sql.expression import func

class LibraryWord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(45), unique=True, nullable=False)

    def __init__(self, word, created_by=None):
        if not LibraryWord.is_valid_word(word):
            raise ValueError("The word %s given to this constructor is not valid." % word)
        self.word = word
        self.created_by = created_by

    '''
    Returns an array of all indexes where the word matches the test_char
    '''
    def has_char(self, test_char, case_sensitive=False):
        positions = []
        word = self.word if case_sensitive else self.word.lower()
        test_char = test_char if case_sensitive else test_char.lower()

        for i, current_char in enumerate(word):
            if current_char == test_char:
                positions += [i]
        return positions

    '''
    Returns whether a given word is valid or not
    '''
    @staticmethod
    def is_valid_word(word):
        return re.match("^[A-Za-z0-9]+$", word)

    '''
    Returns a reandom word from the db
    '''
    @staticmethod
    def get_random():
        query_res = LibraryWord.query.order_by(func.random()).limit(1).first()
        return query_res.word


    

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(6))
    word = db.Column(db.String(45), unique=True, nullable=False)
    db.Column(db.String(45), unique=True, nullable=False)
    guesses = db.relationship("Guess", backref="game", lazy="dynamic")

    def __init__(self, word, created_by=None):
        self.code = uuid.uuid4().hex[:6]
        self.word = word

class Guess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    letter = db.Column(db.String(1), nullable=True)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False )



