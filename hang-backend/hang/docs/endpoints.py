# =====
# define API endpoints for MiniDocs
api_endpoints = [
    {
        'name':'add_word',
        'description':'Adds new word to the hangman library.',
        'url':'word/add/example',
        'urlshow':'/word/add/:word',
        'verb':'PUT',
        'protected':True
    },
    {
        'name':'delete_word',
        'description':'Deletes a word to the hangman library.',
        'url':'/word/delete/example',
        'urlshow':'/word/delete/:word',
        'verb':'DELETE',
        'protected':True
    },
    {
        'name':'start_game',
        'description':'Starts a new hangman game.',
        'url':'/game/start',
        'verb':'GET',
        'protected':False
    },
    {
        'name':'game_check',
        'description':'Checks a letter guess against a given game word.',
        'url':'/game/:id/check',
        'verb':'POST',
        'protected':False
    }
]
