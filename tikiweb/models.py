from django.db import models


# Create your models here.
class Player(models.Model):
    account_id = models.CharField(max_length=50)

    def __str__(self):
        return self.account_id

    class Meta:
        constraints = [models.UniqueConstraint(fields=['account_id'], name='unique_account_id')]


class Season(models.Model):
    display_number = models.IntegerField()
    blizzard_id = models.IntegerField()
    region = models.CharField(max_length=2)
    rating_id = models.IntegerField()

    def __str__(self):
        return f"{self.region} Season #{self.display_number}"

    class Meta:
        constraints = [models.UniqueConstraint(fields=['blizzard_id', 'region'], name='one_season_per_region')]


class Position(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    rank = models.IntegerField()
    rating = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"Season: {self.season.blizzard_id}, Rank {self.rank}: {self.player}, {self.rating}"


