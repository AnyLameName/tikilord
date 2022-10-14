from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from tikiweb import models
import requests


class Command(BaseCommand):
    help = 'Fetches updates for a Battlegrounds leaderboard'

    def add_arguments(self, parser):
        parser.add_argument(
            '--region',
            type=str,
            help='Which region to fetch. Choices: US, AP, EU'
        )

    def handle(self, *args, **options):
        region = options['region']
        self.update_leaderboard(region=region)

    @staticmethod
    def process_row(row):
        player, created = models.Player.objects.get_or_create(account_id=row['accountid'])

        pos = models.Position()
        pos.rank = row['rank']
        pos.rating = row['rating']
        pos.timestamp = timezone.now()
        pos.player = player

        return pos

    @staticmethod
    def get_season(json):
        region = json['region']
        blizzard_id = json['seasonId']
        display_number = blizzard_id + 1
        rating_id = json['seasonMetaData'][region]['battlegrounds']['ratingId']

        season, created = models.Season.objects.get_or_create(
            blizzard_id=blizzard_id,
            region=region,
            defaults={'display_number': display_number, 'rating_id': rating_id}
        )
        return season

    def update_leaderboard(self, region=None, page_count=20):
        regions_to_fetch = []
        if region is None:
            regions_to_fetch = ['US', 'EU', 'AP']
        else:
            regions_to_fetch = [region]

        for r in regions_to_fetch:
            self._update_leaderboard(r, page_count)

    def _update_leaderboard(self, region='US', page_count=20):
        base_url = 'https://hearthstone.blizzard.com/en-us/api/community/leaderboardsData?' \
                   'region={region}&leaderboardId=battlegrounds&page={page}'
        self.stdout.write(f"{timezone.now()} - Fetching top {page_count} pages for {region} - ", ending="")
        for i in range(page_count):
            page_number = i + 1
            if page_number == page_count:
                self.stdout.write(f"{page_number}")
                self.stdout.flush()
            else:
                self.stdout.write(f"{page_number}...", ending="")
                self.stdout.flush()
            continue

            response = requests.get(base_url.format(region=region, page=page_number))
            response.raise_for_status()
            result_json = response.json()

            season = self.get_season(result_json)

            for row in result_json['leaderboard']['rows']:
                position = self.process_row(row)
                position.season = season
                position.save()
