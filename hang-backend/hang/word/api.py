from . import word
from .. import db
from ..models import Word

import re

@word.route('/add/<word>', methods=['PUT'])
def add(word):
    if not Word.is_valid_word(word):
        return "Must be single word, no spaces, numbers or special characters", 400
    w = Word(word)
    db.session.add(w)
    db.session.commit()
    
    return "Word added : " + word, 200


@word.route('/delete/<word>', methods=['DELETE'])
def delete():
    return "Word deleted"


