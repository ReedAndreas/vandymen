from django.db import models

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100, default = '')
    wins = models.IntegerField(default = 0)
    losses = models.IntegerField(default = 0)
    gp = models.IntegerField(default = 0)
    division = models.CharField(max_length = 2)
    abv = models.CharField(max_length = 3)
    average_runs_scored = models.DecimalField(default = 0.0, decimal_places = 3, max_digits = 4)
    average_runs_allowed = models.DecimalField(default = 0.0, decimal_places = 3, max_digits = 4)
    D_value = models.DecimalField(default = 1.0, decimal_places = 3, max_digits = 4)

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

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class GameLog(models.Model):
    date = models.DateField()
    team1 = models.ForeignKey(Team, on_delete = models.DO_NOTHING, null=True, related_name = 'team1')
    team2 = models.ForeignKey(Team, on_delete = models.DO_NOTHING, null=True, related_name = 'team2')
    team_1_victories = models.IntegerField(default = 0)
    team_2_victories = models.IntegerField(default = 0)
    game_1_team1_score = models.IntegerField(default = 0)
    game_1_team2_score = models.IntegerField(default = 0)
    game_2_team1_score = models.IntegerField(default = 0)
    game_2_team2_score = models.IntegerField(default = 0)
    game_3_team1_score = models.IntegerField(default = 0, blank = True)
    game_3_team2_score = models.IntegerField(default = 0, blank = True)

    class Meta:
        ordering = ["-date"]

    def save(self, *args, **kwargs):
        team1 = self.team1
        team2 = self.team2
        team1.wins += self.team_1_victories
        team1.losses += self.team_2_victories
        team2.wins += self.team_2_victories
        team2.losses += self.team_1_victories

        # team 1
        t1_total_runs_scored = team1.gp*team1.average_runs_scored + self.game_1_team1_score + self.game_2_team1_score + self.game_3_team1_score
        t1_total_runs_allowed = team1.gp*team1.average_runs_allowed + self.game_1_team2_score + self.game_2_team2_score + self.game_3_team2_score

        i = 0
        t1_d_total = team1.D_value * team1.gp
        for score in [self.game_1_team1_score, self.game_2_team1_score, self.game_3_team1_score]:
            if (i == self.team_1_victories + self.team_2_victories):
                break
            else:
                if team2.average_runs_allowed == 0:
                    t1_d_total += 1
                else:
                    t1_d_total += score/team2.average_runs_allowed
            i += 1

        team1.gp += self.team_1_victories + self.team_2_victories
        team1.average_runs_scored = t1_total_runs_scored / team1.gp
        team1.D_value = t1_d_total / team1.gp


        # team 2
        t2_total_runs_scored = team2.gp*team2.average_runs_scored + self.game_1_team2_score + self.game_2_team2_score + self.game_3_team2_score
        t2_total_runs_allowed = team2.gp*team2.average_runs_allowed + self.game_1_team1_score + self.game_2_team1_score + self.game_3_team1_score

        i = 0
        t2_d_total = team2.D_value * team2.gp
        for score in [self.game_1_team2_score, self.game_2_team2_score, self.game_3_team2_score]:
            if (i == self.team_1_victories + self.team_2_victories):
                break
            else:
                if team1.average_runs_allowed == 0:
                    t2_d_total += 1
                else:
                    t2_d_total += score/team1.average_runs_allowed
            i += 1

        team2.gp += self.team_1_victories + self.team_2_victories
        team2.average_runs_scored = t2_total_runs_scored / team2.gp
        team2.average_runs_allowed = t2_total_runs_allowed / team2.gp
        team2.D_value = t2_d_total / team2.gp

        team1.average_runs_allowed = t1_total_runs_allowed / team1.gp

        team1.save()
        team2.save()
        super(GameLog, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.team1} ({self.team_1_victories}) vs {self.team2} ({self.team_2_victories}) {self.date}'

class PlayerPerformance(models.Model):
    player = models.ForeignKey(Player, models.DO_NOTHING, null = True)
    game_log = models.ForeignKey(GameLog, on_delete = models.DO_NOTHING, null = True)
    hits = models.IntegerField(default = 0)
    at_bats = models.IntegerField(default = 0)
    doubles = models.IntegerField(default = 0)
    triples = models.IntegerField(default = 0)
    hrs = models.IntegerField(default = 0)
    rbis = models.IntegerField(default = 0)
    k = models.IntegerField(default = 0)
    bb = models.IntegerField(default = 0)

    def calculateOBP(self, hits, walks, ab):
        if ab == 0:
            return 0
        return round((hits + walks) / (ab + walks), 3)

    def calculateSlug(self, single, double, triple, hr, ab):
        if (ab == 0):
            return 0
        return round ((single + 2*double + 3*triple + 4*hr) / ab, 3)

    def save(self, *args, **kwargs):
        p = self.player
        p.ab += self.at_bats
        p.h += self.hits
        p.db += self.doubles
        p.tr += self.triples
        p.hr += self.hrs
        p.rbi += self.rbis
        p.k += self.k
        p.bb += self.bb
        p.ba = round(float(p.h)/p.ab, 3)
        p.obp = self.calculateOBP(p.h, p.bb, p.ab)
        p.sp = self.calculateSlug(p.h - p.db - p.tr - p.hr, p.db, p.tr, p.hr, p.ab)
        p.ops = p.obp + p.sp
        p.gp += self.game_log.team_1_victories + self.game_log.team_2_victories
        p.save()
        super(PlayerPerformance, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.player.name} - {self.game_log}'
