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

def get_random_word():
    """ Choose a word for a game of hangman """
    return 'bananas'

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
        self.game_state = ['_'] * (len(self.word) - 1)
        self.last_guess = None
        self.last_guess_success = False

    def __repr__(self):
        return json.dumps({
            'game_state': self.game_state,
            'complete': self.complete,
            'lives_left': self.lives_left,
            'guesses': self.guesses,
            'lastGuess': self.last_guess,
            'lastGuessSuccess': self.last_guess_success
        })

    def check_complete(self):
        self.complete = '_' not in self.game_state

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
                self.lives_left -= 1
                self.last_guess_success = False

@app.route('/')
def root():
    return 'Server is listening'

@app.route('/games', methods=['POST'])
def create_game():
    """ Create a new game on the server with a unique ID """
    new_game = Hangman()
    return json.dumps({'id': new_game.id})

@app.route('/games/<game_id>/guess_letter', methods=['POST'])
def guess_letter(game_id):
    """ Guess a single letter """
    game = GAMES[game_id]
    data = json.loads(request.data)
    print('request.data', data)
    game.guess(data['guess'])
    return str(game)
