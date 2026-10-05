async function sendJson(url, body) {
    const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });
    const data = await response.json().catch(() => ({ message: 'Unexpected server response' }));
    if (!response.ok) throw new Error(data.message || 'Request failed');
    return data;
}

const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const message = document.getElementById('message');
        try {
            const data = await sendJson('/api/auth/login', {
                username: document.getElementById('username').value,
                password: document.getElementById('password').value
            });
            window.location.href = data.role === 'ADMIN' ? '/admin' : '/player';
        } catch (error) {
            message.textContent = error.message;
        }
    });
}

const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const message = document.getElementById('message');
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        if (password !== confirmPassword) {
            message.textContent = 'Passwords do not match';
            return;
        }
        try {
            const data = await sendJson('/api/auth/register', {
                username: document.getElementById('username').value,
                password
            });
            window.location.href = data.role === 'ADMIN' ? '/admin' : '/player';
        } catch (error) {
            message.textContent = error.message;
        }
    });
}
