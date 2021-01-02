from django.contrib import admin
from .models import Vtuber, On_Live, Reminds

# Register your models here.
class VtuberFrom(admin.ModelAdmin):
	fields = ['uid', 'liver_name', 'production', 'gender']#, 'src'

admin.site.register(Vtuber, VtuberFrom)

class On_liveFrom(admin.ModelAdmin):
	fields = ['uid', 'live_title']

admin.site.register(On_Live, On_liveFrom)

class RemindsFrom(admin.ModelAdmin):
	fields = ['uid', 'start_datetime', 'live_title', 'live_url', 'audience']

admin.site.register(Reminds, RemindsFrom)