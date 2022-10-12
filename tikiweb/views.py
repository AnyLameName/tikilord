from django.http import HttpResponse
from django.template import loader
from django.db.models import Max
import matplotlib.pyplot as plotter
import io, base64
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


def chart(request, account_id):
    season_num = current_season()
    data = {}
    charts = {}
    context = {
        'charts': {},
        'account_id': account_id,
    }
    positions = models.Position.objects.filter(season__blizzard_id=season_num, player__account_id=account_id) \
        .order_by('-timestamp')

    for position in positions:
        region = position.season.region
        if region not in data:
            data[region] = {'rating': [], 'time': []}
        data[region]['rating'].append(position.rating)
        data[region]['time'].append(position.timestamp)

    for region, item in data.items():
        plotter.clf()
        plotter.plot(item['time'], item['rating'], color='blue')
        plotter.title(f"{account_id} - Rating ({region}) v Time")
        plotter.xlabel('Time')
        plotter.xticks(rotation=-25)
        plotter.ylabel('Rating')
        plotter.tight_layout()

        file_obj = io.BytesIO()
        plotter.savefig(file_obj)
        b64 = base64.b64encode(file_obj.getvalue()).decode()
        context['charts'][region] = b64

    template = loader.get_template('tikiweb/chart.html')
    return HttpResponse(template.render(context, request))