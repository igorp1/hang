from flask_testing import TestCase
from flask import url_for
import hang
from hang.models import Word, Game, Guess


class HangTestCase(TestCase):
    def create_app(self):
        return hang.build_app("test")

    def setUp(self):
        self.db = hang.db
        self.db.create_all()

        # Add some words =>
        words = ["3dhubs", "marvin", "print", "filament", "order", "layer"]
        for w in words:
            self.db.session.add( Word(word=w) )
        self.db.session.commit()
        

    def tearDown(self):
        hang.db.session.remove()
        hang.db.drop_all()

    def test_word_add(self):

        WORD_TO_ADD = "Wakanda"

        response = self.client.put(
            url_for("word.add", word=WORD_TO_ADD)
        )
        
        assert response.status_code == 200
        assert  Word.query.filter_by(word=WORD_TO_ADD).first()
        