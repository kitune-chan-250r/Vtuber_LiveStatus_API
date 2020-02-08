from django.contrib import admin
from .models import Vtuber, On_Live

# Register your models here.
class VtuberFrom(admin.ModelAdmin):
	fields = ['uid', 'liver_name', 'production', 'gender', 'src']

admin.site.register(Vtuber, VtuberFrom)

class On_liveFrom(admin.ModelAdmin):
	fields = ['uid', 'live_title']

admin.site.register(On_Live, On_liveFrom)