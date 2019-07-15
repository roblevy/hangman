const baseUrl = 'http://127.0.0.1:5000';
let gameId;

function ajaxRequest(parameterObject) {
  const { url, method, onSuccess, body } = parameterObject;
  const req = new XMLHttpRequest();
  req.open(method || 'GET', baseUrl + url);
  req.onload = onSuccess;
  if (body) {
    req.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
  }
  req.send(JSON.stringify(body));
}

function whenReady(then) {
  return function() {
    if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
      data = JSON.parse(this.responseText);
      then(data);
    }
  }
}

const newButton = document.getElementById('new');
const gameArea = document.getElementById('game');
const guessInput = document.getElementById('guess');
const submitButton = document.getElementById('submit');
const gameStateDiv = document.getElementById('gameState');
const livesDiv = document.getElementById('lives');
const guessesDiv = document.getElementById('guesses');
const victoryDiv = document.getElementById('victory');

function updateGame(res) {
  const { gameState, livesLeft, guesses, complete } = res;
  gameStateDiv.textContent = gameState;
  livesDiv.textContent = 'Lives left: ' + livesLeft;
  guessesDiv.textContent = 'Guesses: ' + guesses;
  victoryDiv.textContent = complete ? 'Victory!' : '';
}

const gamesShow = (gameId) => {
  ajaxRequest({
    url: `/games/${gameId}`,
    onSuccess: whenReady(res => {
      updateGame(res);
    })
  })
}

newButton.addEventListener('click', function() {
  ajaxRequest({
    url: '/games',
    method: 'POST',
    onSuccess: whenReady(res => {
      gameId = res.id;
      gamesShow(gameId);
    })
  })
})

submitButton.addEventListener('click', function() {
  const guessType = guessInput.value.length === 1 ? 'guess_letter' : 'guess_word';
  ajaxRequest({
    url: `/games/${gameId}/${guessType}`,
    method: 'POST',
    body: {
      guess: guessInput.value
    },
    onSuccess: whenReady(res => {
      updateGame(res);
    })
  })
})
