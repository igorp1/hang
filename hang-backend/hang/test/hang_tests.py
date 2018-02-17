from flask_testing import TestCase
from flask import url_for, jsonify
import hang
import os
import json
from hang.models import LibraryWord, Game, Guess, Score
from sqlalchemy import desc


class HangTestCase(TestCase):

    # SETUP/TEARDOWN
    def create_app(self):
        os.environ["APP_ENV"] = "test"
        return hang.build_app("test")

    def setUp(self):
        self.db = hang.db
        self.db.create_all()

        # Add some words =>
        words = ["3dhubs", "marvin", "print", "filament", "order", "layer"]
        for w in words:
            self.db.session.add( LibraryWord(word=w) )
        self.db.session.commit()

    def tearDown(self):
        os.environ["APP_ENV"] = "dev"
        hang.db.session.remove()
        hang.db.drop_all()

    # MISC
    def test_require_key_decorator(self):
        # no key 
        response = self.client.put( url_for("word.add", word="Killmonger") )
        assert response.status_code == 401

        # adding key
        KEY = "TEST_KEY"
        word_to_add = "Wakanda"
        response = self.client.put( url_for("word.add", word=word_to_add, key=KEY) )
        assert response.status_code == 200
        assert LibraryWord.query.filter_by(word=word_to_add).first()

    # WORD TESTS
    def test_word_is_valid(self):

        assert LibraryWord.is_valid_word("numb34s")
        assert LibraryWord.is_valid_word("simple")
        assert not LibraryWord.is_valid_word("two words")
        assert not LibraryWord.is_valid_word("wh@t?")

    def test_word_has_letter(self):
        # letter that exists
        word = LibraryWord.query.filter_by(word="3dhubs").first()
        char = 'h'
        expected_result = [2]
        assert word.has_char(char) == expected_result

        # letter that exists not case sensitive
        word = LibraryWord.query.filter_by(word="3dhubs").first()
        char = 'H'
        expected_result = [2]
        assert word.has_char(char) == expected_result

        # letter that doesn't exist
        word = LibraryWord.query.filter_by(word="3dhubs").first()
        char = 'x'
        expected_result = []
        assert word.has_char(char) == expected_result

        # a number
        word = LibraryWord.query.filter_by(word="3dhubs").first()
        char = '3'
        expected_result = [0]
        assert word.has_char(char) == expected_result

        # more than one return
        word = LibraryWord.query.filter_by(word="order").first()
        char = 'r'
        expected_result = [1, 4]
        assert word.has_char(char) == expected_result

    def test_word_get_random(self):
        words = ["3dhubs", "marvin", "print", "filament", "order", "layer"]
        assert LibraryWord.get_random() in words

        # if you want to check randomness you can run:
        # "nosetests --nocapture" to see the output
        check_words = False
        if check_words:
            print "\n=== test_word_get_random ===="
            for i in range(0,10):
                print LibraryWord.get_random()
            print "=============================\n"

    def test_word_add(self):
        
        KEY = "TEST_KEY"
        word_to_add = "Wakanda"
        response = self.client.put( url_for("word.add", word=word_to_add, key=KEY) )
        assert response.status_code == 200
        assert LibraryWord.query.filter_by(word=word_to_add).first()

    def test_word_delete(self):
        KEY = "TEST_KEY"
        word_to_remove = "filament"
        response = self.client.delete( url_for("word.delete", word=word_to_remove, key=KEY) )
        assert response.status_code == 200
        assert not LibraryWord.query.filter_by(word=word_to_remove).first()
        
    # GAME TESTS
    def test_game_by_code(self):
        # make new game
        g = Game("molding")
        self.db.session.add(g)
        self.db.session.commit()

        # get by code
        CODE = g.code
        g_test = Game.by_code(CODE)
        assert g == g_test

    def test_game_start(self):
        
        response = self.client.get( url_for("game.new") )
        assert response.status_code == 200

        response_expected_fields = ["word_length","game_code"]
        body = json.loads(response.get_data(as_text=True))

        for x in response_expected_fields:
            assert x in body

    def test_game_check(self):

        # create game => 
        g = Game.start_new()
        game_code = g.code
        word = g.word

        # check a letter that doesn't belongs to the game word 
        L1 = 'X' # we know for sure none of the words contain X
        response = self.client.post( url_for("game.check", code=game_code),
                                    data=json.dumps(dict(guess=L1)),  
                                    content_type='application/json')
        assert response.status_code == 200

        result = json.loads(response.get_data(as_text=True))
        assert result['found'] == False
        assert result['positions'] == []
        assert result['status'] == 'playing'

        # check a char that belongs to the game word 
        L2 = word[0] # on the setup all first chars are unique to the word
        response = self.client.post( url_for("game.check", code=game_code),
                                    data=json.dumps(dict(guess=L2)),  
                                    content_type='application/json')
        assert response.status_code == 200

        result = json.loads(response.get_data(as_text=True))
        assert result['found'] == True
        assert result['positions'] == [0]
        assert result['status'] == 'playing'

        # check a char that belongs to the game word more than once
        L3 = word[0] # on the setup all first chars are unique to the word
        response = self.client.post( url_for("game.check", code=game_code),
                                    data=json.dumps(dict(guess=L3)),
                                    content_type='application/json')
        assert response.status_code == 400

        # check a character that is not valid
        L4 = '?'
        response = self.client.post( url_for("game.check", code=game_code),
                                    data=json.dumps(dict(guess=L4)),
                                    content_type='application/json')
        assert response.status_code == 400

    def test_game_load(self):

        # create game => 
        g = Game.start_new()
        game_code = g.code
        word = g.word

        # load a game that does not exist
        response = self.client.get( url_for("game.load", code='X') )
        assert response.status_code == 404

        # verify the info on the game you created
        response = self.client.get( url_for("game.load", code=game_code) )
        assert response.status_code == 200

        result = json.loads(response.get_data(as_text=True))
        
        assert result['status'] == 'playing'
        assert result['attempts'] == []
        assert result['wordLength'] == len(word)
        assert result['foundChars'] == {}
        assert result['mistakeCount'] == 0

        # after a guess
        L1 = word[0]
        response = self.client.post( url_for("game.check", code=game_code),
                                    data=json.dumps(dict(guess=L1)),
                                    content_type='application/json')
        assert response.status_code == 200

        response = self.client.get( url_for("game.load", code=game_code) )
        assert response.status_code == 200

        result = json.loads(response.get_data(as_text=True))
        assert result['status'] == 'playing'
        assert result['attempts'] == [ L1 ]
        assert result['wordLength'] == len(word)
        assert L1 in result['foundChars']
        assert result['foundChars'][L1] == [0]
        assert result['mistakeCount'] == 0

    def test_game_challenge(self):
        word = 'element'

        response = self.client.post( url_for("game.challenge"),
                                    data=json.dumps(dict(word=word)),
                                    content_type='application/json')
        assert response.status_code == 200

        result = response.get_data(as_text=True)
        assert result
        assert Game.by_code(result).word == word

    def test_game_long_word(self):
        W = "12345678901234567890123456789012345678901234567890"
        g = Game(W)
        self.db.session.add(g)
        self.db.session.commit()

        for x in range(0,10):
            g.check_guess(str(x))

        assert g.status == "won"

    # SCORE 
    def test_score_save(self):
        # create game 
        g = Game.start_new()
        game_code = g.code
        g.word = 'EASY'
        self.db.session.commit()

        # play
        g.check_guess('E')
        g.check_guess('A')
        g.check_guess('S')
        g.check_guess('Y')

        assert g.status == 'won'

        # save score
        player = "T'Challa"
        response = self.client.post( url_for("leaderboard.save"),
                                    data=json.dumps(dict(player=player, game=g.code)),
                                    content_type='application/json')
        assert response.status_code == 200

        s = Score.query.order_by(desc(Score.id)).first()

        assert s.player == player
        assert s.word == g.word
        assert s.score == g.calculate_score()

    def test_score_get(self):

        # make game
        g = Game('Amsterdam')
        self.db.session.add(g)
        self.db.session.commit()

        # mock scores
        s1 = Score('PLAYER 1', g)
        s1.score = 100
        self.db.session.add(s1)
        s2 = Score('PLAYER 2', g)
        s2.score = 30
        self.db.session.add(s2)
        s3 = Score('PLAYER 3', g)
        s3.score = 112
        self.db.session.add(s3)
        s4 = Score('PLAYER 4', g) 
        s4.score = 10
        self.db.session.add(s4)
        self.db.session.commit()

        response = self.client.get( url_for("leaderboard.load") )

        assert response.status_code == 200

        result = json.loads(response.get_data(as_text=True))

        assert len(result) == 4
        assert result[0]['player'] == s3.player
        assert result[0]['word'] == g.word
        assert result[3]['player'] == s4.player
        

        

    