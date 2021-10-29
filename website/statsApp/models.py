from django.db import models

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100, default = '')
    wins = models.IntegerField(default = 0)
    losses = models.IntegerField(default = 0)
    gp = models.IntegerField(default = 0)
    division = models.CharField(max_length = 2)
    abv = models.CharField(max_length = 3)

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=100, default = '')
    team = models.ForeignKey(Team, on_delete = models.CASCADE, null=True)
    gp = models.IntegerField(default = 0)
    ab = models.IntegerField(default = 0)
    h = models.IntegerField(default = 0)
    db = models.IntegerField(default = 0)
    tr = models.IntegerField(default = 0)
    hr = models.IntegerField(default = 0)
    rbi = models.IntegerField(default = 0)
    k = models.IntegerField(default = 0)
    bb = models.IntegerField(default = 0)
    ba = models.DecimalField(default = 0.0, decimal_places = 3, max_digits = 4)
    sp = models.DecimalField(default = 0.0, decimal_places = 3, max_digits = 4)
    obp = models.DecimalField(default = 0.0, decimal_places = 3, max_digits = 4)
    ops = models.DecimalField(default = 0.0, decimal_places = 3, max_digits = 4)

    def __str__(self):
        return self.name
