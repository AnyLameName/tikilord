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

    def update_leaderboard(self, region='US', page_count=25):
        base_url = 'https://hearthstone.blizzard.com/en-us/api/community/leaderboardsData?' \
                   'region={region}&leaderboardId=battlegrounds&page={page}'
        self.stdout.write(f"Fetching top {page_count} pages for {region}...")
        for i in range(page_count):
            page_number = i + 1
            if page_number % 10 == 0 or page_number == page_count:
                self.stdout.write(f"\tFetching page {page_number}")

            response = requests.get(base_url.format(region=region, page=page_number))
            response.raise_for_status()
            result_json = response.json()

            season = self.get_season(result_json)

            for row in result_json['leaderboard']['rows']:
                position = self.process_row(row)
                position.season = season
                position.save()
        self.stdout.write("Done.")
