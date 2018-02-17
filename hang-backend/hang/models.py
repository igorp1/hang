import uuid, re
from hang import db
from sqlalchemy import desc
from sqlalchemy.sql.expression import func

class LibraryWord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(45), unique=True, nullable=False)

    def __init__(self, word, created_by=None):
        if not LibraryWord.is_valid_word(word):
            raise ValueError("The word %s given to this constructor is not valid." % word)
        self.word = word

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
    code = db.Column(db.String(6), unique=True)
    word = db.Column(db.String(45), nullable=False)
    status = db.Column(db.String(10), nullable=False, default='playing') # playing|won|lost
    guesses = db.relationship("Guess", backref="game", lazy="dynamic")

    def __init__(self, word):
        self.code = uuid.uuid4().hex[:6]
        self.word = word
        self.status = 'playing'

    '''
    Sets the status of the game based on all of the guesses
    '''
    def set_status(self):
        if self.count_wrong_guesses() >= 5:
            self.status = 'lost'
        elif self.count_chars_found() == len(self.word):
            self.status = 'won'
        else:
            self.status = 'playing' # no change here
        db.session.commit()
        
    '''
    Returns how many wrong guesses  
    '''
    def count_wrong_guesses(self):
        fails_count = 0
        for x in self.guesses:
            res = LibraryWord(self.word).has_char( x.letter )
            if res == []: fails_count += 1
        return fails_count

    '''
    Returns how many characters were found in the word. rep
    '''
    def count_chars_found(self):
        count = 0
        positions = self.get_found_positions()
        for x in positions:
            count += len(positions[x])
        return count

    '''
    Returns an array of all the position 
    '''
    def get_found_positions(self):
        found_arr = dict()
        for x in self.guesses:
            positions = LibraryWord(self.word).has_char( x.letter )
            if positions:
                found_arr[x.letter] = positions
        return found_arr

    '''
    Returns an object with the result of checking the guess
    '''
    def check_guess(self, guess):
        
        # commit guess
        guess_obj = Guess(guess, self.code)
        db.session.add(guess_obj)
        db.session.commit()

        # check position
        positions = LibraryWord(self.word).has_char(guess)

        # evaluate and set current status
        self.set_status()

        return {
            "found":len(positions)>0,
            "positions":positions,
            "status":self.status,
        }

    '''
    Return the guesses as an array of strings
    '''
    def get_array_of_guesses(self):
        guesses_arr = []
        for x in self.guesses:
            guesses_arr += [x.letter]
        return guesses_arr

    '''
    Return an object with all necessary information to load it from scratch 
    '''
    def get_load_object(self):
        return dict(
            status = self.status,
            attempts = self.get_array_of_guesses(),
            wordLength = len(self.word),
            foundChars = self.get_found_positions(),
            mistakeCount = self.count_wrong_guesses()
        )

    '''
    Calculates the score of a given game
    '''
    def calculate_score(self):
        if(self.status == 'playing' or self.status == 'lost'):
            return 0
        else:
            L = len(self.word)
            F = self.count_chars_found()
            M = self.count_wrong_guesses()
            G = L + M
            calculated_score = round(100*(F - M)/(L+G))
            return calculated_score if calculated_score > 0 else 0

    '''
    Returns the game object of a given code
    '''
    @staticmethod
    def by_code(code):
        return Game.query.filter_by(code=code).first()

    '''
    Creates a new game and returns its object 
    '''
    @staticmethod 
    def start_new():
        word = LibraryWord.get_random()
        game = Game(word)
        db.session.add(game)
        db.session.commit()
        return game

    '''
    Creates a "challenge" game with a given word.
    '''
    @staticmethod 
    def make_challenge_from_word(word):
        game = Game(word)
        db.session.add(game)
        db.session.commit()
        return game.code

class Guess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    letter = db.Column(db.String(1), nullable=True) #obs, could also be a number
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False )

    def __init__(self, guess, game_code):
        if not Guess.is_valid(guess):
            raise ValueError("The guess (%s) passed to this contructor is not a valid." % guess)
        if Guess.is_guess_on_game(guess, game_code):
            raise ValueError("The guess (%s) has already been guessed on this game." % guess)
        self.letter = guess
        self.game_id = Game.by_code(game_code).id

    '''
    Returns whether a given guess is valid or not. Expects single letter or digit
    '''
    @staticmethod
    def is_valid(guess):
        return re.match("[a-zA-Z0-9]{1}$", guess)

    '''
    Returns whether a character has been guessed in a game  
    '''
    @staticmethod
    def is_guess_on_game(guess, game_code):
        g = Game.by_code(game_code)
        return bool( g.guesses.filter_by(letter=guess).first() )

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player = db.Column(db.String(6))
    word = db.Column(db.String(45))
    score = db.Column(db.Integer)

    def __init__(self, player, game):
        self.player = player
        self.word = game.word
        self.score = game.calculate_score()

    def serialize(self):
        return {
            "id" : self.id,
            "player" : self.player,
            "word" : self.word,
            "score" : self.score, 
        }

    @staticmethod
    def get_top(limit_num=10, serialize=True):
        query_res = Score.query.order_by(desc(Score.score)).limit(limit_num).all()
        if not serialize:
            return query_res
        else:
            score_arr = []
            for s in query_res:
                score_arr += [s.serialize()]
            return score_arr


