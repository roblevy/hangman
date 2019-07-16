# Simple hangman

A simple-as-possible client-server hangman game. It's built in Python/Flask on the back-end and vanilla Javascript/HTML/CSS on the front-end.

## Running the game

The easiest way to start the server is:

```
FLASK_APP=server.py python -m flask run
```

And since the front-end makes Ajax requests to the back-end you should probably serve that too. This can be easily done with:

```
cd src
python3 -m http.server
```

or

```
python -m SimpleHTTPServer
```

## The game always gives me one-letter words!

The random word API I've used is not really production-ready. (I didn't make it!) The API keys seem to expire every now and then.

If this happens, you'll only ever get the 'word' "w" (which is the first letter of 'wrong API key'!)

You can get a new key [here](https://random-word-api.herokuapp.com/key?) and insert it the top of the `server.py` file here:

```
GAMES = {}
LIFE_COUNT = 9
WORDS_API_KEY = 'HAOCOQQR' # <-- Insert the new API key here!
```
