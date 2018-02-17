# =====
# define API endpoints for MiniDocs
api_endpoints = [
    {
        'name':'New Game',
        'description':'Starts a new hangman game.',
        'url':'/game/new',
        'verb':'GET',
        'protected':False
    },
    {
        'name':'Check Game',
        'description':'Checks a letter guess against a given game word.',
        'urlshow':'/game/:code/check',
        'url':'game/nc7kA0/check',
        'verb':'POST',
        'protected':False
    },
    {
        'name':'Load Game',
        'description':'Loads a game given its code.',
        'urlshow':'/game/:code/load',
        'url':'game/nc7kA0/load',
        'verb':'GET',
        'protected':False
    },
    {
        'name':'Make challenge',
        'description':'Allows user to create challenege game.',
        'urlshow':'/game/challenge',
        'url':'game/load',
        'verb':'POST',
        'protected':False
    },
    {
        'name':'Save to Leaderboard',
        'description':'Saves a player\'s score',
        'urlshow':'/game/challenge',
        'url':'game/load',
        'verb':'POST',
        'protected':False
    },
    {
        'name':'Load Leaderboard',
        'description':'Loads top 10 players.',
        'urlshow':'/game/challenge',
        'url':'game/load',
        'verb':'GET',
        'protected':False
    },
    {
        'name':'Add Word',
        'description':'Adds new word to the hangman library.',
        'url':'word/add/example',
        'urlshow':'/word/add/:word',
        'verb':'PUT',
        'protected':True
    },
    {
        'name':'Delete Word',
        'description':'Deletes a word to the hangman library.',
        'url':'/word/delete/example',
        'urlshow':'/word/delete/:word',
        'verb':'DELETE',
        'protected':True
    },
]
