from django.http import HttpResponse
from django.urls import path, re_path
from django.views.static import serve

from game import views
from django.conf import settings

urlpatterns = [
    path('', views.home),
    path('login', views.login_page),
    path('register', views.register_page),
    path('player', views.player_page),
    path('admin', views.admin_page),
    path('favicon.ico', lambda r: HttpResponse(status=204)),
    path('api/auth/register', views.register_api),
    path('api/auth/login', views.login_api),
    path('api/auth/logout', views.logout_api),
    path('api/game/start', views.start_game_api),
    path('api/game/status', views.game_status_api),
    path('api/game/active', views.active_game_api),
    path('api/game/<int:game_id>/guess', views.guess_api),
    path('api/admin/report/day', views.day_report_api),
    path('api/admin/report/user', views.user_report_api),
    path('api/admin/words', views.words_api),
    # Serve CSS/JS even when DEBUG is off (small app, no separate web server needed)
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.BASE_DIR / 'static'}),
]
