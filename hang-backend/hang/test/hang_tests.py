from flask_testing import TestCase
from flask import url_for
import hang
import os
from hang.models import LibraryWord, Game, Guess


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
        print "\n=== test_word_get_random ===="
        for i in range(0,10):
            print LibraryWord.get_random()
        print "=============================\n"

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
        
    