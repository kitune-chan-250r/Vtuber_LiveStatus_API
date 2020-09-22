from django.db import models

# Create your models here.

class Vtuber(models.Model):
    uid = models.CharField(max_length=50, primary_key=True, unique=True)
    liver_name = models.CharField(max_length=100)
    production = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    #src = models.CharField(max_length=200, default='None')


class On_Live(models.Model):
    uid = models.ForeignKey(Vtuber, on_delete=models.CASCADE, primary_key=True, unique=True)
    start_time = models.DateTimeField(auto_now_add=True)
    live_title = models.CharField(max_length=100)
    live_url = models.CharField(max_length=100)


class LiveLog(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    uid = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    production = models.CharField(max_length=100)


'''class ScheduledLive(models.Model):
    uid = models.ForeignKey(Vtuber, on_delete=models.CASCADE, primary_key=True, unique=True)
    start_time = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    live_url = models.CharField(max_length=100)
'''
