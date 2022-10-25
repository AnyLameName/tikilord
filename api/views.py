from django.db.models import Max
from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plotter
import matplotlib.dates as mpl_dates
from matplotlib import font_manager
import io
import base64
import json
from . import models


def current_season():
    return models.Season.objects.aggregate(Max('blizzard_id'))['blizzard_id__max']


# Create your views here.
def top(request, region='US', player_count=25):
    # Make sure we only get data from the most recent season.
    season_num = current_season()

    # TODO: This seems to produce valid JSON, but a proper serializer is definitely required.
    # Look into django's rest_framework.
    response = { 'top': [],}
    for position in models.Position.objects.filter(season__blizzard_id=season_num, rank__lte=player_count, season__region=region)\
        .order_by('rank', '-timestamp').distinct('rank'):
        response['top'].append({'account_id': position.player.account_id, 'rank': position.rank, 'rating': position.rating})
    return HttpResponse(json.dumps(response), content_type='application/json')


def top_chart(request, region='US', player_count=16):
    # Make sure we only get data from the most recent season.
    season_num = current_season()

    # Top N final positions
    top_n = models.Position.objects.filter(season__blizzard_id=season_num, rank__lte=player_count,
                                          season__region=region) \
        .order_by('rank', '-timestamp').distinct('rank')

    # Can't possibly be the best way to do this, but now get the full season data for those top 16 players.
    data = {}
    for entry in top_n:
        # List comprehension?

        data[entry.player.account_id] = {
            'ratings': [],
            'time': [],
        }
        positions = models.Position.objects.filter(season__blizzard_id=season_num,
                                                   season__region=region,
                                                   player__account_id=entry.player.account_id)
        for p in positions:
            data[entry.player.account_id]['ratings'].append(p.rating)
            data[entry.player.account_id]['time'].append(p.timestamp)

    context = {
        'region': region,
        'player_count': player_count,
    }
    # Chart all the different players
    plotter.clf()
    plotter.title(f"Top {player_count} - {region}")

    font = font_manager.FontProperties(fname='/home/jgagnon/fonts/noto-sans/NotoSansCJKtc-Regular.otf')

    for player_name, player_data in data.items():
        plotter.plot(player_data['time'], player_data['ratings'], label=player_name)
    plotter.legend(bbox_to_anchor=(1.03, 1.02), prop=font)
    plotter.xticks(rotation=-45)
    plotter.gca().xaxis.set_major_formatter(mpl_dates.DateFormatter('%m-%d-%y'))
    plotter.grid(linewidth=0.5, linestyle='--')

    # Turn plot into image and encode for transit
    file_obj = io.BytesIO()
    plotter.savefig(file_obj, bbox_inches='tight', dpi=200)
    b64 = base64.b64encode(file_obj.getvalue()).decode()
    context['chart'] = b64

    #TODO: Once again, this works but should be properly serialized.
    response = { 'img': b64}
    return HttpResponse(json.dumps(response), content_type='application/json')


def player_by_id(request, account_id):
    season_num = current_season()
    history = {}
    positions = models.Position.objects.filter(season__blizzard_id=season_num, player__account_id=account_id)\
        .order_by('-timestamp')

    for position in positions:
        region = position.season.region
        if region not in history:
            history[region] = []
        history[region].append(position)

    context = {
        'account_id': account_id,
        'history': history,
    }
    return render(request, 'api/player.html', context)


def chart(request, account_id):
    season_num = current_season()
    data = {}
    charts = {}
    context = {
        'charts': {},
        'account_id': account_id,
    }
    positions = models.Position.objects.filter(season__blizzard_id=season_num, player__account_id=account_id) \
        .order_by('timestamp')

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

    return render(request, 'api/chart.html', context)