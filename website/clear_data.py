import numpy as np
import pandas as pd

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')

import django
django.setup()

print('Are you sure you would like to clear all player and team data (y/n): ', end = '')
sure = input()

if sure == 'y':
    from statsApp.models import Player, Team
    for p in Player.objects.all():
        p.gp = 0
        p.ab = 0
        p.h = 0
        p.db = 0
        p.tr = 0
        p.hr = 0
        p.rbi = 0
        p.k = 0
        p.bb = 0
        p.ba = 0
        p.sp = 0
        p.obp = 0
        p.ops = 0
        p.save()

    for t in Team.objects.all():
            t.wins = 0
            t.losses = 0
            t.gp = 0
            t.average_runs_scored = 0
            t.average_runs_allowed = 0
            t.D_value = 1
            t.save()
