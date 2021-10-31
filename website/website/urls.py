"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from statsApp import views
from statsApp.models import Player, Team
from statsApp.views import PlayerListView, PlayerDetailView, TeamsListView, TeamDetailView, GameLogDetailView

team_players_dict = {str(t.pk): [] for t in Team.objects.all()}
for t in Team.objects.all():
    for p in Player.objects.filter(team=t.pk):
        team_players_dict[str(t.pk)].append(p)


urlpatterns = [
    path('', views.landing, name = 'landing'),
    path('players/', PlayerListView.as_view(extra_context={'players_page': 'active'})),
    path('teams/', TeamsListView.as_view(extra_context={'teams_page': 'active'})),
    path('series/<int:pk>/', GameLogDetailView.as_view(extra_context={})),
    path('stats/', views.stats, name = 'stats'),
    path('matchup_prediction/', views.matchup_prediction, name = 'matchup_prediction'),
    path('FAQ/', views.FAQ, name = 'FAQ'),
    path('admin/', admin.site.urls),
    path('standings/', views.standings, name = 'standings'),
    path('mock_draft/', views.mock_draft, name = 'mock_draft'),
    path('players/<int:pk>/', PlayerDetailView.as_view(extra_context={'players_page': 'active'}), name='player-detail'),
    path('teams/<int:pk>/', TeamDetailView.as_view(extra_context={'teams_page': 'active', 'players': team_players_dict}), name='team-detail'),
]
