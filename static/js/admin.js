function esc(v) {
    return String(v).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

const dayDate = document.getElementById('dayDate');
const dayResult = document.getElementById('dayResult');
const userResult = document.getElementById('userResult');
const wordInput = document.getElementById('wordInput');
const wordMessage = document.getElementById('wordMessage');
const wordList = document.getElementById('wordList');
const wordCount = document.getElementById('wordCount');

{
    const d = new Date();
    dayDate.value = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

async function loadWords() {
    const response = await fetch('/api/admin/words');
    const data = await response.json();
    if (!response.ok) {
        wordList.textContent = data.message || 'Could not load words';
        return;
    }

    wordCount.textContent = data.words.length;
    wordList.innerHTML = data.words.length
        ? data.words.map(word => `<span class="word-chip">${esc(word)}</span>`).join('')
        : '<p class="muted">No words found in the database.</p>';
}

document.getElementById('dayReportBtn').addEventListener('click', async () => {
    const response = await fetch(`/api/admin/report/day?date=${encodeURIComponent(dayDate.value)}`);
    const data = await response.json();
    if (!response.ok) {
        dayResult.textContent = data.message || 'Could not load report';
        return;
    }
    dayResult.innerHTML = `
        <div class="metric">Users: <strong>${data.users}</strong></div>
        <div class="metric">Words tried: <strong>${data.wordsTried}</strong></div>
        <div class="metric">Correct guesses: <strong>${data.correctGuesses}</strong></div>
    `;
});

document.getElementById('userReportBtn').addEventListener('click', async () => {
    const username = document.getElementById('reportUsername').value.trim();
    const response = await fetch(`/api/admin/report/user?username=${encodeURIComponent(username)}`);
    const data = await response.json();
    if (!response.ok) {
        userResult.textContent = data.message || 'Could not load report';
        return;
    }
    if (!data.rows.length) {
        userResult.innerHTML = '<p class="muted">No games found for this user.</p>';
        return;
    }
    const rows = data.rows.map(row => `
        <tr>
            <td>${esc(row.date)}</td>
            <td>${row.wordsTried}</td>
            <td>${row.correctGuesses}</td>
            <td>${row.guessSubmissions}</td>
        </tr>`).join('');
    userResult.innerHTML = `
        <h3>${esc(data.username)}</h3>
        <table class="report-table">
            <thead><tr><th>Date</th><th>Words Tried</th><th>Correct Guesses</th><th>Total Guess Submissions</th></tr></thead>
            <tbody>${rows}</tbody>
        </table>
    `;
});

document.getElementById('addWordBtn').addEventListener('click', async () => {
    const word = wordInput.value.trim().toUpperCase();
    wordMessage.textContent = '';

    if (!/^[A-Z]{5}$/.test(word)) {
        wordMessage.textContent = 'Enter exactly 5 English letters.';
        return;
    }

    const response = await fetch('/api/admin/words', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ word })
    });
    const data = await response.json();

    if (!response.ok) {
        wordMessage.textContent = data.message || 'Could not add word';
        return;
    }

    wordMessage.textContent = `${data.word} added successfully.`;
    wordInput.value = '';
    await loadWords();
});

wordInput.addEventListener('input', () => {
    wordInput.value = wordInput.value.toUpperCase().replace(/[^A-Z]/g, '').slice(0, 5);
});

document.getElementById('logoutBtn').addEventListener('click', async () => {
    await fetch('/api/auth/logout', { method: 'POST' });
    window.location.href = '/login';
});

loadWords();
