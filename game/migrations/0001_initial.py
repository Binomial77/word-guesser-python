from django.db import migrations, models
import django.db.models.deletion

# The bundled word-guess-game.db already contains these tables, so the SQL uses
# IF NOT EXISTS: `python manage.py migrate` works on both the old DB and a brand-new one.
SQL = [
    "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE COLLATE BINARY, password_hash TEXT NOT NULL, role TEXT NOT NULL CHECK (role IN ('ADMIN','PLAYER')), created_at TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS words (id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT NOT NULL UNIQUE)",
    "CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, secret_word_id INTEGER NOT NULL, played_date TEXT NOT NULL, attempts_used INTEGER NOT NULL DEFAULT 0, won INTEGER NOT NULL DEFAULT 0, finished INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL, completed_at TEXT, FOREIGN KEY (user_id) REFERENCES users(id), FOREIGN KEY (secret_word_id) REFERENCES words(id))",
    "CREATE TABLE IF NOT EXISTS guesses (id INTEGER PRIMARY KEY AUTOINCREMENT, game_id INTEGER NOT NULL, guess_number INTEGER NOT NULL, guessed_word TEXT NOT NULL, submitted_at TEXT NOT NULL, FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE, UNIQUE (game_id, guess_number))",
    "CREATE INDEX IF NOT EXISTS idx_games_user_date ON games(user_id, played_date)",
    "CREATE INDEX IF NOT EXISTS idx_games_date ON games(played_date)",
    "CREATE INDEX IF NOT EXISTS idx_guesses_game ON guesses(game_id)",
]

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[migrations.RunSQL(q, migrations.RunSQL.noop) for q in SQL],
            state_operations=[
                migrations.CreateModel(name='User', fields=[('id', models.BigAutoField(primary_key=True, serialize=False)), ('username', models.CharField(max_length=255, unique=True)), ('password_hash', models.TextField()), ('role', models.CharField(max_length=20)), ('created_at', models.CharField(max_length=40))], options={'db_table': 'users'}),
                migrations.CreateModel(name='Word', fields=[('id', models.BigAutoField(primary_key=True, serialize=False)), ('word', models.CharField(max_length=5, unique=True))], options={'db_table': 'words'}),
                migrations.CreateModel(name='Game', fields=[('id', models.BigAutoField(primary_key=True, serialize=False)), ('played_date', models.CharField(max_length=10)), ('attempts_used', models.IntegerField(default=0)), ('won', models.BooleanField(default=False)), ('finished', models.BooleanField(default=False)), ('created_at', models.CharField(max_length=40)), ('completed_at', models.CharField(blank=True, max_length=40, null=True)), ('secret_word', models.ForeignKey(db_column='secret_word_id', on_delete=django.db.models.deletion.PROTECT, to='game.word')), ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.PROTECT, to='game.user'))], options={'db_table': 'games'}),
                migrations.CreateModel(name='Guess', fields=[('id', models.BigAutoField(primary_key=True, serialize=False)), ('guess_number', models.IntegerField()), ('guessed_word', models.CharField(max_length=5)), ('submitted_at', models.CharField(max_length=40)), ('game', models.ForeignKey(db_column='game_id', on_delete=django.db.models.deletion.CASCADE, to='game.game'))], options={'db_table': 'guesses'}),
            ],
        ),
    ]
