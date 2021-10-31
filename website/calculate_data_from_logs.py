import numpy as np
import pandas as pd

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')

import django
django.setup()

from statsApp.models import Player, Team, PlayerPerformance, GameLog

for g in GameLog.objects.all():
    g.save()

for p in PlayerPerformance.objects.all():
    p.save()
