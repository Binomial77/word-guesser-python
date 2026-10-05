# Word Guess Game

A Wordle-style web game built with Django and SQLite. Players try to guess a hidden 5-letter word, and an admin can view reports and manage the word list.

## What the project does

### For players
- Register a new account or log in.
- Start a game: the server picks a random secret 5-letter word.
- Each game allows up to **5 guesses**, and each player can start up to **3 games per day**.
- After every guess, each letter is colored:
  - **Green**: right letter, right position
  - **Yellow**: letter is in the word, but in a different position
  - **Gray**: letter is not in the word
- If you lose, the game reveals the secret word.
- If you reload the page in the middle of a game, your game and earlier guesses are restored.

### For the admin
- **Day Report**: for a chosen date, shows the number of users who played, games played, and games won.
- **User Report**: for a chosen username, shows games played, games won, and total guesses submitted, per day.
- **Game Words**: view all words in the database and add new 5-letter words.

### Account rules
- **Username**: at least 5 letters (A-Z or a-z only).
- **Password**: at least 5 characters, containing letters, a number, and at least one of `$`, `%` or `*`.

## Requirements
- Python 3.10 or newer
- pip

## How to run

1. Open a terminal in the project folder.

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # macOS / Linux
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database and start the server:

   ```bash
   python manage.py migrate
   python manage.py runserver 8080
   ```

5. Open **http://127.0.0.1:8080** in your browser.

## Logging in

| Role   | Username    | Password    |
|--------|-------------|-------------|
| Admin  | `AdminUser` | `Admin$123` |
| Player | Create one from the **Register** page | - |

Admins are sent to `/admin`, and players are sent to `/player`.

## Configuration (optional)

Settings can be changed with environment variables:

| Variable | Default | Purpose |
|----------|---------|---------|
| `APP_ADMIN_USERNAME` | `AdminUser` | Admin username |
| `APP_ADMIN_PASSWORD` | `Admin$123` | Admin password |
| `DJANGO_SECRET_KEY` | `dev-secret-change-me` | Secret key for sessions (change it in production) |
| `DJANGO_DEBUG` | `true` | Set to `false` in production |
| `DJANGO_ALLOWED_HOSTS` | `127.0.0.1,localhost` | Comma-separated list of allowed hosts |

Daily game limit and guesses per game are set in `word_guess_game/settings.py` (`DAILY_LIMIT = 3`, `MAX_GUESSES = 5`).

Example (macOS / Linux):

```bash
APP_ADMIN_PASSWORD='MyNew$Pass1' python manage.py runserver 8080
```

## Pages and API

**Pages**

| URL | Description |
|-----|-------------|
| `/` | Redirects to the right page, or shows login |
| `/login`, `/register` | Authentication pages |
| `/player` | Game page (players) |
| `/admin` | Admin dashboard (admin only) |

**API**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Create a player account |
| POST | `/api/auth/login` | Log in |
| POST | `/api/auth/logout` | Log out |
| POST | `/api/game/start` | Start a new game |
| GET | `/api/game/status` | Games remaining today |
| GET | `/api/game/active` | Current unfinished game, if any |
| POST | `/api/game/<id>/guess` | Submit a guess |
| GET | `/api/admin/report/day?date=YYYY-MM-DD` | Day report (admin) |
| GET | `/api/admin/report/user?username=NAME` | User report (admin) |
| GET / POST | `/api/admin/words` | List or add words (admin) |

## Project structure

```
word-guess-game/
├── manage.py
├── requirements.txt
├── word-guess-game.db        SQLite database (users, words, games, guesses)
├── game/                     Backend app
│   ├── models.py             Database models
│   ├── services.py           Game rules, validation, reports
│   ├── views.py              Pages and API endpoints
│   ├── middleware.py         Login and admin-access checks
│   └── migrations/
├── word_guess_game/          Project settings and URL routes
├── templates/                HTML pages (login, register, player, admin)
└── static/                   CSS and JavaScript
```

## Troubleshooting

- **Page has no styling or buttons do nothing**: make sure you started the server with `python manage.py runserver 8080` from the project folder, then hard-refresh the browser (Ctrl+F5).
- **Port already in use**: run on another port, e.g. `python manage.py runserver 8000`.
- **"Invalid HTTP_HOST header"**: add your host name to `DJANGO_ALLOWED_HOSTS`.
- **Forgot the admin password**: the `APP_ADMIN_PASSWORD` variable only applies when the admin account is first created. To reset it, delete the `AdminUser` row from the `users` table (or delete the database file), then restart the server with the new `APP_ADMIN_PASSWORD`.
- **Start fresh**: stop the server, delete `word-guess-game.db`, then run the steps in "How to run" again. Default words and the admin account are created automatically.

## Notes
- This project is intended for local use and learning. Before deploying publicly, set a strong `DJANGO_SECRET_KEY`, set `DJANGO_DEBUG=false`, and add CSRF protection.