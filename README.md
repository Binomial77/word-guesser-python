# Word Guess Game — Django

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8080
```

Open http://127.0.0.1:8080

`migrate` is safe on the bundled `word-guess-game.db` (existing data is kept) and also creates all tables on a brand-new database.

Default admin: `AdminUser` / `Admin$123` (override with `APP_ADMIN_USERNAME` / `APP_ADMIN_PASSWORD`).

## Rules
- 3 games per day, 5 guesses per game; a game in progress is restored after a page reload.
- Username: 5+ letters. Password: 5+ chars with letters, a number and one of `$ % *`.

## Structure
- `game/` models, views, services, auth middleware, migration
- `word_guess_game/` project settings and URLs
- `templates/` HTML, `static/` CSS and JS
