from django.db import models
class User(models.Model):
    id=models.BigAutoField(primary_key=True); username=models.CharField(max_length=255,unique=True); password_hash=models.TextField(); role=models.CharField(max_length=20); created_at=models.CharField(max_length=40)
    class Meta: db_table='users'
class Word(models.Model):
    id=models.BigAutoField(primary_key=True); word=models.CharField(max_length=5,unique=True)
    class Meta: db_table='words'
class Game(models.Model):
    id=models.BigAutoField(primary_key=True); user=models.ForeignKey(User,db_column='user_id',on_delete=models.PROTECT); secret_word=models.ForeignKey(Word,db_column='secret_word_id',on_delete=models.PROTECT); played_date=models.CharField(max_length=10); attempts_used=models.IntegerField(default=0); won=models.BooleanField(default=False); finished=models.BooleanField(default=False); created_at=models.CharField(max_length=40); completed_at=models.CharField(max_length=40,null=True,blank=True)
    class Meta: db_table='games'
class Guess(models.Model):
    id=models.BigAutoField(primary_key=True); game=models.ForeignKey(Game,db_column='game_id',on_delete=models.CASCADE); guess_number=models.IntegerField(); guessed_word=models.CharField(max_length=5); submitted_at=models.CharField(max_length=40)
    class Meta: db_table='guesses'
