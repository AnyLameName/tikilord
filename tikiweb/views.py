from django.http import HttpResponse
from django.template import loader
from django.db.models import Max
from . import models


def current_season():
    return models.Season.objects.aggregate(Max('blizzard_id'))['blizzard_id__max']


# Create your views here.
def top(request, region='US', player_count=25):
    # Make sure we only get data from the most recent season.
    season_num = current_season()

    positions = models.Position.objects.filter(season__blizzard_id=season_num, rank__lte=player_count, season__region=region)\
        .order_by('rank', '-timestamp').distinct('rank')
    template = loader.get_template('tikiweb/index.html')
    context = {
        'top': positions,
    }
    return HttpResponse(template.render(context, request))


def player(request, account_id):
    season_num = current_season()
    history = {}
    positions = models.Position.objects.filter(season__blizzard_id=season_num, player__account_id=account_id)\
        .order_by('-timestamp')

    for position in positions:
        region = position.season.region
        if region not in history:
            history[region] = []
        history[region].append(position)

    template = loader.get_template('tikiweb/player.html')
    context = {
        'account_id': account_id,
        'history': history,
    }
    return HttpResponse(template.render(context, request))
