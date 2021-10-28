from django.shortcuts import render
from .models import Player, Team
import statsApp.df_manipulation as dfm
from django.views.generic import ListView
from django.views.generic import DetailView


# setup dataframe
df = dfm.get_df(Player.objects.all())

byHR = df.sort_values('hr', ascending = False).iloc[0:10][['name', 'hr']]
byBA = df.sort_values('ba', ascending = False).iloc[0:10][['name', 'ba']]
byOPS = df.sort_values('ops', ascending = False).iloc[0:10][['name', 'ops']]

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
