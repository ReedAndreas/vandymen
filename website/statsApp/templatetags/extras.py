from django import template
from django.template.defaulttags import register
from statsApp.models import Player, Team

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def from_index(list, i):
    return list[i:]

@register.simple_tag
def get_team_members(pk):
    return list(Player.objects.filter(team = pk))

@register.simple_tag
def get_gb(top, wins, losses):
    if wins == '' or losses == '':
        return ''
    if float(wins) + float(losses) == 0:
        return top
    else:
        dif = (float(wins) - float(losses))/2
    return round(top - dif, 1)

@register.simple_tag
def get_team_abv(val):
    return Team.objects.get(pk=val).abv

@register.simple_tag
def get_wp(w, l):
    if w == '':
        return ''

    if w + l == 0:
        return '0.000'
    elif l == 0:
        return '1.000'
    else:
        return '{:.3f}'.format(w/(l+w))
