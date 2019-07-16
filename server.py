from flask import Flask, request
from flask_cors import CORS
import requests
import random
import uuid
import json
import re

app = Flask(__name__)
CORS(app)

GAMES = {}
LIFE_COUNT = 9
WORDS_API_KEY = 'HAOCOQQR'

def get_random_word():
    """ Choose a word for a game of hangman """
    url = 'https://random-word-api.herokuapp.com/word'
    params = {
        'key': WORDS_API_KEY,
        'number': 1
    }
    res = requests.get(url, params=params)
    word = res.json()[0]
    print(word)
    return word

class Hangman():
    """ A representation of a single game of hangman """
    def __init__(self):
        game_id = str(uuid.uuid4())
        GAMES[game_id] = self
        self.id = game_id
        self.word = get_random_word()
        self.guesses = []
        self.lives_left = LIFE_COUNT
        self.complete = False
        self.game_state = ['_'] * len(self.word)
        self.last_guess = None
        self.last_guess_success = False

    def __repr__(self):
        return json.dumps({
            'gameState': self.game_state,
            'complete': self.complete,
            'livesLeft': self.lives_left,
            'guesses': self.guesses,
            'lastGuess': self.last_guess,
            'lastGuessSuccess': self.last_guess_success
        })

    def check_complete(self):
        self.complete = '_' not in self.game_state

    def lose_life(self):
        """ After an incorrect guess """
        self.lives_left -= 1
        self.last_guess_success = False

    def guess(self, letter):
        """ Guess a single letter """
        self.last_guess = letter
        if not letter in self.guesses:
            # This is a new guess
            self.guesses.append(letter)
            if re.search(letter, self.word):
                # The guess has found a match!
                for match in re.finditer(letter, self.word):
                    self.game_state[match.start()] = letter
                self.check_complete()
                self.last_guess_success = True
            else:
                # The guess was wrong
                self.lose_life()

    def guess_word(self, word):
        """ Attempt the whole word """
        print('Attempting word guess', word, self.word)
        if word == self.word:
            self.complete = True
            self.game_state = list(self.word)
            self.last_guess_success = True
        else:
            self.lose_life()

@app.route('/')
def root():
    return 'Server is listening'

@app.route('/games', methods=['POST'])
def games_create():
    """ Create a new game on the server with a unique ID """
    new_game = Hangman()
    return json.dumps({'id': new_game.id})

@app.route('/games/<game_id>/guess_letter', methods=['POST'])
def guess_letter(game_id):
    """ Guess a single letter """
    try:
        game = GAMES[game_id]
    except KeyError:
        return not_found()
    data = json.loads(request.data)
    game.guess(data['guess'])
    return str(game)

@app.route('/games/<game_id>/guess_word', methods=['POST'])
def guess_word(game_id):
    """ Guess the word """
    try:
        game = GAMES[game_id]
    except KeyError:
        return not_found()
    data = json.loads(request.data)
    game.guess_word(data['guess'])
    return str(game)

@app.route('/games')
def games_index():
    return json.dumps(list(GAMES.keys()))

@app.route('/games/<game_id>')
def games_show(game_id):
    try:
        game = GAMES[game_id]
        return str(game)
    except KeyError:
        return not_found()

def not_found():
    """ A 404 for a game which doesn't exist on the server """
    return json.dumps({'message': 'No such game'}), 404
