let currentGameId = null;
let gameFinished = false;

const startBtn = document.getElementById('startBtn');
const gameArea = document.getElementById('gameArea');
const board = document.getElementById('board');
const guessForm = document.getElementById('guessForm');
const guessInput = document.getElementById('guessInput');
const gamesLeft = document.getElementById('gamesLeft');
const guessesLeft = document.getElementById('guessesLeft');
const gameMessage = document.getElementById('gameMessage');
const logoutBtn = document.getElementById('logoutBtn');

function addEmptyRow() {
    for (let i = 0; i < 5; i++) {
        const tile = document.createElement('div');
        tile.className = 'tile';
        board.appendChild(tile);
    }
}

function startBoard() {
    board.innerHTML = '';
    for (let i = 0; i < 5; i++) addEmptyRow();
}

async function refreshStatus() {
    const response = await fetch('/api/game/status');
    if (!response.ok) return;
    const data = await response.json();
    gamesLeft.textContent = data.gamesRemainingToday;
    startBtn.disabled = data.gamesRemainingToday === 0;
}

startBtn.addEventListener('click', async () => {
    gameMessage.textContent = '';
    const response = await fetch('/api/game/start', { method: 'POST' });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
        gameMessage.textContent = data.message || 'Could not start game';
        return;
    }
    currentGameId = data.gameId;
    gameFinished = false;
    gameArea.classList.remove('hidden');
    startBoard();
    guessesLeft.textContent = data.maxGuesses;
    gamesLeft.textContent = data.gamesRemainingToday;
    guessInput.disabled = false;
    guessForm.querySelector('button').disabled = false;
    guessInput.value = '';
    guessInput.focus();
});

guessInput.addEventListener('input', () => {
    guessInput.value = guessInput.value.replace(/[^A-Za-z]/g, '').toUpperCase().slice(0, 5);
});

guessForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!currentGameId || gameFinished) return;
    const word = guessInput.value.trim().toUpperCase();
    if (!/^[A-Z]{5}$/.test(word)) {
        gameMessage.textContent = 'Enter exactly 5 letters.';
        return;
    }

    const response = await fetch(`/api/game/${currentGameId}/guess`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ word })
    });
    const data = await response.json();
    if (!response.ok) {
        gameMessage.textContent = data.message || 'Could not submit guess';
        return;
    }

    fillRow(data.attemptNumber - 1, data.evaluation);

    guessesLeft.textContent = data.attemptsRemaining;
    guessInput.value = '';
    gameMessage.textContent = data.message;

    if (data.finished) {
        gameFinished = true;
        guessInput.disabled = true;
        guessForm.querySelector('button').disabled = true;
        await function fillRow(row, evaluation) {
    evaluation.forEach((item, index) => {
        const tile = board.children[row * 5 + index];
        tile.textContent = item.letter;
        tile.classList.add(item.status.toLowerCase());
    });
}

async function resumeActiveGame() {
    const response = await fetch('/api/game/active');
    if (!response.ok) return;
    const data = await response.json();
    if (!data.game) return;
    currentGameId = data.game.gameId;
    gameFinished = false;
    gameArea.classList.remove('hidden');
    startBoard();
    data.game.evaluations.forEach((evaluation, row) => fillRow(row, evaluation));
    guessesLeft.textContent = data.game.attemptsRemaining;
    gameMessage.textContent = 'Game in progress restored.';
}

refreshStatus();
resumeActiveGame();
        window.setTimeout(() => alert(data.message), 50);
    }
});

logoutBtn.addEventListener('click', async () => {
    await fetch('/api/auth/logout', { method: 'POST' });
    window.location.href = '/login';
});

function fillRow(row, evaluation) {
    evaluation.forEach((item, index) => {
        const tile = board.children[row * 5 + index];
        tile.textContent = item.letter;
        tile.classList.add(item.status.toLowerCase());
    });
}

async function resumeActiveGame() {
    const response = await fetch('/api/game/active');
    if (!response.ok) return;
    const data = await response.json();
    if (!data.game) return;
    currentGameId = data.game.gameId;
    gameFinished = false;
    gameArea.classList.remove('hidden');
    startBoard();
    data.game.evaluations.forEach((evaluation, row) => fillRow(row, evaluation));
    guessesLeft.textContent = data.game.attemptsRemaining;
    gameMessage.textContent = 'Game in progress restored.';
}

refreshStatus();
resumeActiveGame();
