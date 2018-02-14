from . import word
from .. import db
from ..helpers import require_key
from ..models import LibraryWord

@word.route('/add/<word>', methods=['PUT'])
@require_key
def add(word):
    if not LibraryWord.is_valid_word(word):
        return "Must be single word, no spaces, numbers or special characters", 400
    w = LibraryWord(word)
    db.session.add(w)
    db.session.commit()
    return "Word added", 200

@require_key
@word.route('/delete/<word>', methods=['DELETE'])
def delete(word):
    LibraryWord.query.filter_by(word=word).delete()
    return "Word deleted", 200


