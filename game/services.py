import base64, hashlib, hmac, re, secrets
from datetime import date, datetime
from django.conf import settings
from django.db import transaction
from .models import User,Word,Game,Guess

def now_text(): return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
def hash_password(p):
 s=secrets.token_bytes(16); d=hashlib.pbkdf2_hmac('sha256',p.encode(),s,120000,32); return f'{base64.b64encode(s).decode()}:{base64.b64encode(d).decode()}'
def password_matches(p,stored):
 try:
  a,b=stored.split(':',1); return hmac.compare_digest(base64.b64decode(b),hashlib.pbkdf2_hmac('sha256',p.encode(),base64.b64decode(a),120000,32))
 except Exception:return False
def login(u,p):
 u=(u or '').strip(); p=p or ''
 try:x=User.objects.get(username=u)
 except User.DoesNotExist:raise ValueError('Invalid username or password')
 if not password_matches(p,x.password_hash):raise ValueError('Invalid username or password')
 return x
def register_player(u,p):
 u=(u or '').strip(); p=p or ''
 if not u or not re.fullmatch(r'[A-Za-z]{5,}',u):raise ValueError('Username must contain at least 5 letters and use only A-Z or a-z')
 if not p or not re.fullmatch(r'(?=.*[A-Za-z])(?=.*\d)(?=.*[$%*])[A-Za-z\d$%*]{5,}',p):raise ValueError('Password must be at least 5 characters and contain letters, a number, and one of $, % or *')
 if User.objects.filter(username__iexact=u).exists():raise ValueError('Username already exists')
 return User.objects.create(username=u,password_hash=hash_password(p),role='PLAYER',created_at=now_text())
def seed_data():
 for w in ['ABOUT','OTHER','WHICH','THEIR','THERE','WOULD','THESE','CLICK','WORLD','HOUSE','LIGHT','BRAVE','PLANT','GREEN','MONEY','WATER','APPLE','TABLE','TRAIN','MUSIC']:Word.objects.get_or_create(word=w)
 if not User.objects.filter(username=settings.ADMIN_USERNAME).exists():User.objects.create(username=settings.ADMIN_USERNAME,password_hash=hash_password(settings.ADMIN_PASSWORD),role='ADMIN',created_at=now_text())
@transaction.atomic
def start_game(uid):
 active=Game.objects.filter(user_id=uid,finished=False).order_by('-id').first()
 if active:raise RuntimeError('You already have a game in progress. Finish it first.')
 today=date.today().isoformat(); used=Game.objects.filter(user_id=uid,played_date=today).count()
 if used>=settings.DAILY_LIMIT:raise RuntimeError(f'You have already used all {settings.DAILY_LIMIT} games for today')
 w=Word.objects.order_by('?').first()
 if not w:raise RuntimeError('No words are configured in the database')
 g=Game.objects.create(user_id=uid,secret_word_id=w.id,played_date=today,created_at=now_text())
 return {'gameId':g.id,'gamesRemainingToday':settings.DAILY_LIMIT-used-1,'maxGuesses':settings.MAX_GUESSES}
def evaluate(secret,guess):
 st=['ABSENT']*5; rem={}
 for i in range(5):
  if secret[i]==guess[i]:st[i]='CORRECT'
  else:rem[secret[i]]=rem.get(secret[i],0)+1
 for i in range(5):
  if st[i]=='CORRECT':continue
  if rem.get(guess[i],0):st[i]='PRESENT';rem[guess[i]]-=1
 return [{'letter':guess[i],'status':st[i]} for i in range(5)]
@transaction.atomic
def submit_guess(uid,gid,word):
 g=(word or '').strip()
 if not re.fullmatch(r'[A-Z]{5}',g):raise ValueError('Guess must be exactly 5 uppercase letters')
 try:game=Game.objects.select_related('secret_word').get(id=gid)
 except Game.DoesNotExist:raise ValueError('Game not found')
 if game.user_id!=uid:raise ValueError('This game does not belong to the logged-in user')
 if game.finished:raise RuntimeError('This game is already finished')
 n=game.attempts_used+1; won=game.secret_word.word==g; finished=won or n==settings.MAX_GUESSES
 Guess.objects.create(game_id=gid,guess_number=n,guessed_word=g,submitted_at=now_text())
 game.attempts_used=n;game.won=won;game.finished=finished;game.completed_at=now_text() if finished else None;game.save()
 return {'evaluation':evaluate(game.secret_word.word,g),'attemptNumber':n,'attemptsRemaining':settings.MAX_GUESSES-n,'won':won,'finished':finished,'message':'Congratulations! You guessed the word.' if won else f'Better luck next time! The word was {game.secret_word.word}.' if finished else 'Keep going!'}
def games_remaining_today(uid):return max(0,settings.DAILY_LIMIT-Game.objects.filter(user_id=uid,played_date=date.today().isoformat()).count())
def day_report(d):
 try:date.fromisoformat(d)
 except:raise ValueError('Date must be in YYYY-MM-DD format')
 q=Game.objects.filter(played_date=d);return {'date':d,'users':q.values('user_id').distinct().count(),'wordsTried':q.count(),'correctGuesses':q.filter(won=True).count()}
def user_report(u):
 try:x=User.objects.get(username=u)
 except User.DoesNotExist:raise ValueError('User not found')
 rows=[]
 for d in Game.objects.filter(user_id=x.id).values_list('played_date',flat=True).distinct().order_by('-played_date'):
  q=Game.objects.filter(user_id=x.id,played_date=d);rows.append({'date':d,'wordsTried':q.count(),'correctGuesses':q.filter(won=True).count(),'guessSubmissions':Guess.objects.filter(game__user_id=x.id,game__played_date=d).count()})
 return rows
def add_word(w):
 v=(w or '').strip().upper()
 if not re.fullmatch(r'[A-Z]{5}',v):raise ValueError('Word must contain exactly 5 English letters')
 if Word.objects.filter(word=v).exists():raise ValueError('Word already exists in the database')
 Word.objects.create(word=v);return v

def active_game(uid):
 g=Game.objects.filter(user_id=uid,finished=False).select_related('secret_word').order_by('-id').first()
 if not g:return None
 rows=[evaluate(g.secret_word.word,x.guessed_word) for x in Guess.objects.filter(game_id=g.id).order_by('guess_number')]
 return {'gameId':g.id,'evaluations':rows,'attemptsRemaining':settings.MAX_GUESSES-g.attempts_used,'maxGuesses':settings.MAX_GUESSES}
