import json
from django.http import JsonResponse,HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_GET,require_POST
from .models import User,Word
from .services import *
def body(r):
 try:d=json.loads(r.body or '{}')
 except Exception:return {}
 return d if isinstance(d,dict) else {}
def home(r):
 u=getattr(r,'current_user',None)
 return HttpResponseRedirect('/admin' if u.role=='ADMIN' else '/player') if u else render(r,'login.html')
def login_page(r):
 u=getattr(r,'current_user',None)
 return HttpResponseRedirect('/admin' if u.role=='ADMIN' else '/player') if u else render(r,'login.html')
def register_page(r):
 u=getattr(r,'current_user',None)
 return HttpResponseRedirect('/admin' if u.role=='ADMIN' else '/player') if u else render(r,'register.html')
def player_page(r):return render(r,'player.html')
def admin_page(r):return render(r,'admin.html')
@require_GET
def active_game_api(r):return JsonResponse({'game':active_game(r.current_user.id)})
@require_POST
def register_api(r):
 try:b=body(r);u=register_player(b.get('username'),b.get('password'));r.session.flush();r.session['user_id']=u.id;return JsonResponse({'message':'Registration successful','role':u.role,'username':u.username})
 except ValueError as e:return JsonResponse({'message':str(e)},status=400)
@require_POST
def login_api(r):
 try:b=body(r);u=login(b.get('username'),b.get('password'));r.session.flush();r.session['user_id']=u.id;return JsonResponse({'message':'Login successful','role':u.role,'username':u.username})
 except ValueError as e:return JsonResponse({'message':str(e)},status=400)
@require_POST
def logout_api(r):r.session.flush();return JsonResponse({'message':'Logged out'})
@require_POST
def start_game_api(r):
 try:return JsonResponse(start_game(r.current_user.id))
 except RuntimeError as e:return JsonResponse({'message':str(e)},status=400)
@require_GET
def game_status_api(r):return JsonResponse({'gamesRemainingToday':games_remaining_today(r.current_user.id)})
@require_POST
def guess_api(r,game_id):
 try:return JsonResponse(submit_guess(r.current_user.id,game_id,body(r).get('word')))
 except (ValueError,RuntimeError) as e:return JsonResponse({'message':str(e)},status=400)
@require_GET
def day_report_api(r):
 try:return JsonResponse(day_report(r.GET.get('date')))
 except ValueError as e:return JsonResponse({'message':str(e)},status=400)
@require_GET
def user_report_api(r):
 try:return JsonResponse({'username':r.GET.get('username'),'rows':user_report(r.GET.get('username'))})
 except ValueError as e:return JsonResponse({'message':str(e)},status=400)
def words_api(r):
 if r.method=='GET':return JsonResponse({'words':list(Word.objects.order_by('word').values_list('word',flat=True))})
 if r.method=='POST':
  try:return JsonResponse({'message':'Word added successfully','word':add_word(body(r).get('word'))})
  except ValueError as e:return JsonResponse({'message':str(e)},status=400)
 return JsonResponse({'detail':'Method not allowed'},status=405)
