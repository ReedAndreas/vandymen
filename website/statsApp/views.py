from django.shortcuts import render
from .models import Player, Team
import statsApp.df_manipulation as dfm
from django.views.generic import ListView
from django.views.generic import DetailView


# setup dataframe
df = dfm.get_df(Player.objects.all())

byHR = df[df['ab'] > 5].sort_values('hr', ascending = False).iloc[0:10][['name', 'hr']]
byBA = df[df['ab'] > 5].sort_values('ba', ascending = False).iloc[0:10][['name', 'ba']]
byOPS = df[df['ab'] > 5].sort_values('ops', ascending = False).iloc[0:10][['name', 'ops']]

byHRlist = list(byHR.to_dict('records'))
byBAlist = list(byBA.to_dict('records'))
byOPSlist = list(byOPS.to_dict('records'))

hrRankList = sorted(list(dict(byHR['hr']).values()))[::-1]
baRankList = sorted(list(dict(byBA['ba']).values()))[::-1]
OPSRankList = sorted(list(dict(byOPS['ops']).values()))[::-1]

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

# Create your views here.
def landing(request):
    my_dict = {'byHR': byHRlist, 'byBA': byBAlist, 'byOPS': byOPSlist, "home_page": 'active'}

    def get_name(request):
        if request.method == 'POST':
            print('yes')

    return render(request,'landing.html', context=my_dict)

def standings(request):

    nl_teams = list(Team.objects.filter(division = 'NL'))
    al_teams = list(Team.objects.filter(division = 'AL'))

    nl_teams = sorted(nl_teams, key = lambda x : x.wins - .001 * x.losses, reverse = True)
    al_teams = sorted(al_teams, key = lambda x : x.wins - .001 * x.losses, reverse = True)

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

    my_dict = {'al_teams' : al_teams, 'nl_teams' : nl_teams, 'standings_page' : 'active'}
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

class PlayerListView(ListView):
    model = Player
    ordering = ['name']

class TeamsListView(ListView):
    model = Team
    ordering = ['name']

class PlayerDetailView(DetailView):
    queryset = Player.objects.all()

class TeamDetailView(DetailView):
    queryset = Team.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team_pk = Team.objects.get(name = self.object)
        context['players'] = list(Player.objects.filter(team=team_pk))
        return context
