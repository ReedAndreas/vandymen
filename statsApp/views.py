from django.shortcuts import render
from .models import Player, Team, PlayerPerformance, GameLog
import statsApp.df_manipulation as dfm
from django.views.generic import ListView
from django.views.generic import DetailView
from .forms import MatchupPredictor
from django.http import HttpResponse, HttpResponseRedirect
import numpy as np
import pandas as pd
import plotly.express as px


# Create your views here.
def landing(request):
    my_dict = {"home_page": 'active'}

    return render(request,'landing.html', context=my_dict)

def stats(request):
    # setup dataframe
    df = dfm.get_df(Player.objects.all())

    byHR = df[df['ab'] > 5].sort_values('hr', ascending = False).iloc[0:10][['name', 'hr']]
    byBA = df[df['ab'] > 5].sort_values('ba', ascending = False).iloc[0:10][['name', 'ba']]
    byOPS = df[df['ab'] > 5].sort_values('ops', ascending = False).iloc[0:10][['name', 'ops']]
    byH = df[df['ab'] > 5].sort_values('h', ascending = False).iloc[0:10][['name', 'h']]
    byRBI = df[df['ab'] > 5].sort_values('rbi', ascending = False).iloc[0:10][['name', 'rbi']]

    byHRlist = list(byHR.to_dict('records'))
    byBAlist = list(byBA.to_dict('records'))
    byOPSlist = list(byOPS.to_dict('records'))
    byHlist = list(byH.to_dict('records'))
    byRBIlist = list(byRBI.to_dict('records'))

    hrRankList = sorted(list(dict(byHR['hr']).values()))[::-1]
    baRankList = sorted(list(dict(byBA['ba']).values()))[::-1]
    OPSRankList = sorted(list(dict(byOPS['ops']).values()))[::-1]
    hRankList = sorted(list(dict(byH['h']).values()))[::-1]
    rbiRankList = sorted(list(dict(byRBI['rbi']).values()))[::-1]

    for p in byHRlist:
        for i in range(len(hrRankList)):
            if p['hr'] == hrRankList[i]:
                p['rank'] = i+1
                break
        p['pk'] = Player.objects.get(name = p['name']).pk

    for p in byBAlist:
        for i in range(len(baRankList)):
            if p['ba'] == baRankList[i]:
                p['rank'] = i+1
                break
        p['pk'] = Player.objects.get(name = p['name']).pk

    for p in byOPSlist:
        for i in range(len(OPSRankList)):
            if p['ops'] == OPSRankList[i]:
                p['rank'] = i+1
                break
        p['pk'] = Player.objects.get(name = p['name']).pk

    for p in byHlist:
        for i in range(len(hRankList)):
            if p['h'] == hRankList[i]:
                p['rank'] = i+1
                break
        p['pk'] = Player.objects.get(name = p['name']).pk

    for p in byRBIlist:
        for i in range(len(rbiRankList)):
            if p['rbi'] == rbiRankList[i]:
                p['rank'] = i+1
                break
        p['pk'] = Player.objects.get(name = p['name']).pk


    my_dict = {'byHR': byHRlist, 'byBA': byBAlist, 'byOPS': byOPSlist, 'byH': byHlist, 'byRBI': byRBIlist, "stats_page": 'active'}

    return render(request,'stats.html', context=my_dict)

def standings(request):

    nl_teams = list(Team.objects.filter(division = 'NL'))
    al_teams = list(Team.objects.filter(division = 'AL'))

    nl_teams = sorted(nl_teams, key = lambda x : (x.wins - x.losses)/2, reverse = True)
    al_teams = sorted(al_teams, key = lambda x : (x.wins - x.losses)/2, reverse = True)

    nl_teams = [[n, 0] for n in nl_teams]
    al_teams = [[a, 0] for a in al_teams]


    ind = 0
    for t in nl_teams:
        pos_val = t[0].wins - .001 * t[0].losses
        c = 0
        for p in nl_teams:
            c += 1
            if pos_val == p[0].wins - .001 * p[0].losses:
                nl_teams[ind][1] = c
                ind += 1
                break

    ind = 0
    for t in al_teams:
        pos_val = t[0].wins - .001 * t[0].losses
        c = 0
        for p in al_teams:
            c += 1
            if pos_val == p[0].wins - .001 * p[0].losses:
                al_teams[ind][1] = c
                ind += 1
                break

    nl_teams.insert(3, {'warning': 'table-warning'})
    al_teams.insert(3, {'warning': 'table-warning'})

    nl_top = (nl_teams[0][0].wins - nl_teams[0][0].losses)/2
    al_top = (al_teams[0][0].wins - al_teams[0][0].losses)/2

    my_dict = {'al_teams' : al_teams, 'nl_teams' : nl_teams, 'standings_page' : 'active', 'al_top' : al_top, 'nl_top' : nl_top}
    return render(request,'standings.html', context=my_dict)



def mock_draft(request):
    df = dfm.get_erg(list(Player.objects.all()), list(Team.objects.all()))
    players_list = []
    for index, row in df.iterrows():
        players_list.append(Player.objects.get(name = row['name']))
    rounds = []
    players_list = players_list[0:56]
    for i in range(0, len(players_list), 14):
        rounds.append(players_list[i: i+14])

    for r in range(len(rounds)):
        for p in range(len(rounds[r])):
            rounds[r][p] = [p+1, rounds[r][p]]
        rounds[r] = [r+1, rounds[r]]

    my_dict = {'rounds': rounds}
    return render(request,'mock_draft.html', context=my_dict)

def FAQ(request):
    my_dict = {}
    return render(request,'FAQ.html', context=my_dict)

class PlayerListView(ListView):
    model = Player
    ordering = ['name']

class TeamsListView(ListView):
    model = Team
    ordering = ['name']

    team_players_dict = {str(t.pk): [] for t in Team.objects.all()}

    def get_context_data(self, **kwargs):
        context = super(TeamsListView,self).get_context_data(**kwargs)
        team_players_dict = {}
        for t in Team.objects.all():
            team_players_dict[str(t.pk)] = []
            for p in Player.objects.filter(team=t.pk):
                team_players_dict[str(t.pk)].append(p)

        context['players'] = team_players_dict
        return context

class PlayerDetailView(DetailView):
    queryset = Player.objects.all()

class GameLogDetailView(DetailView):
    queryset = GameLog.objects.all()
    def get_context_data(self, **kwargs):
        team1 = Team.objects.get(name = self.object.team1)
        team2 = Team.objects.get(name = self.object.team2)
        performances = list(self.object.playerperformance_set.all())
        team1_performances = []
        team2_performances = []
        for p in performances:
            if p.player.team == team1:
                team1_performances.append(p)
            elif p.player.team == team2:
                team2_performances.append(p)

        games = [] # will store games in (w/l, team1, team2, score) format

        i = 0
        for scores in [[self.object.game_1_team1_score, self.object.game_1_team2_score], [self.object.game_2_team1_score, self.object.game_2_team2_score],
                [self.object.game_3_team1_score, self.object.game_3_team2_score]]:
            if i == self.object.team_1_victories + self.object.team_2_victories:
                break
            if scores[0] > scores[1]:
                # home win
                games.append(['W', team1.abv, team2.abv, f'{scores[0]} - {scores[1]}'])
            else:
                games.append(['L', team1.abv, team2.abv, f'{scores[0]} - {scores[1]}'])
            i += 1

        context = {'team1_performances': team1_performances, 'team2_performances': team2_performances, 'games': games, 'team1pk': team1.pk, 'team2pk': team2.pk,
                    'team_1_victories': self.object.team_1_victories, 'team_2_victories': self.object.team_2_victories}
        return context


class TeamDetailView(DetailView):
    queryset = Team.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team_pk = Team.objects.get(name = self.object)
        context['players'] = list(Player.objects.filter(team=team_pk))
        recent_series = list(self.object.team1.all()) + list(self.object.team2.all())
        recent_series.sort(key = lambda x : x.date, reverse = True)

        series_summaries = []
        for s in recent_series:
            if s.team1 == self.object:
                curr_team_wins = s.team_1_victories
                opps_team_wins = s.team_2_victories
                opp_team = s.team2.abv
                opp_teampk = s.team2.pk
            elif s.team2 == self.object:
                curr_team_wins = s.team_2_victories
                opps_team_wins = s.team_1_victories
                opp_team = s.team1.abv
                opp_teampk = s.team1.pk
            result = 'L'
            if curr_team_wins > opps_team_wins:
                result = 'W'
            series_summaries.append([result, opp_team, f'{curr_team_wins} - {opps_team_wins}', opp_teampk, s.pk])

        context['recent_series'] = series_summaries

        return context

def matchup_prediction(request):
    form = MatchupPredictor
    my_dict = {'form': form}
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MatchupPredictor(request.POST)
        # check whether it's valid:
        if form.is_valid():
            team1_obj = Team.objects.get(name = form.cleaned_data['team1'])
            team2_obj = Team.objects.get(name = form.cleaned_data['team2'])

            team_1_estimate = team1_obj.D_value * np.sqrt(team1_obj.average_runs_scored) * np.sqrt(team2_obj.average_runs_allowed)
            team_2_estimate = team2_obj.D_value * np.sqrt(team2_obj.average_runs_scored) * np.sqrt(team1_obj.average_runs_allowed)

            if form.cleaned_data['team1'] == form.cleaned_data['team2']:
                pass
            elif team_1_estimate == 0 or team_2_estimate == 0:
                pass
            else:
                sd = 2.8
                team_1_wins = 0
                num_iters = 1000
                team_1_estimate = np.sqrt(team_1_estimate)
                team_2_estimate = np.sqrt(team_2_estimate)
                for i in range(num_iters):
                    team_1_random = np.random.normal(team_1_estimate, sd)
                    team_2_random = np.random.normal(team_2_estimate, sd)
                    if team_1_random > team_2_random:
                        team_1_wins += 1
                    elif team_1_random == team_2_random:
                        i -= 1

                graph = px.pie(labels = [team1_obj.name, team2_obj.name], values = [team_1_wins, num_iters-team_1_wins],
                            hole = 0.7, names = [team1_obj.name, team2_obj.name], height = 300, width= 370,
                            color_discrete_sequence = ["goldenrod", "black"], hover_data=None).to_html()

                my_dict['graph'] = graph

    return render(request,'matchup_prediction.html', context=my_dict)
