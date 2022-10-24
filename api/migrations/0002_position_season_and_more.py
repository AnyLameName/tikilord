# Generated by Django 4.1.1 on 2022-10-10 03:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField()),
                ('rating', models.IntegerField()),
                ('timestamp', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_number', models.IntegerField()),
                ('blizzard_id', models.IntegerField()),
                ('region', models.CharField(max_length=2)),
                ('rating_id', models.IntegerField()),
            ],
        ),
        migrations.RenameField(
            model_name='player',
            old_name='display_name',
            new_name='account_id',
        ),
        migrations.AddConstraint(
            model_name='player',
            constraint=models.UniqueConstraint(fields=('account_id',), name='unique_account_id'),
        ),
        migrations.AddConstraint(
            model_name='season',
            constraint=models.UniqueConstraint(fields=('blizzard_id', 'region'), name='one_season_per_region'),
        ),
        migrations.AddField(
            model_name='position',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.player'),
        ),
        migrations.AddField(
            model_name='position',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.season'),
        ),
    ]
