# Generated by Django 2.2.4 on 2019-11-06 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_livelog'),
    ]

    operations = [
        migrations.AddField(
            model_name='vtuber',
            name='src',
            field=models.CharField(default='None', max_length=200),
        ),
    ]
