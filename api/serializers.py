from rest_framework import serializers
from .models import Vtuber, On_Live, Reminds

class VtuberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vtuber
        fields = ('uid', 'liver_name', 'production', 'gender')#, 'src'


class OnLiveSerializer(serializers.ModelSerializer):
    uid = VtuberSerializer()
    class Meta:
        model = On_Live
        fields = ('uid', 'start_time', 'live_title', 'live_url')

#uidのみでPOSTするためのシリアライザ
class OnLive_POST_Serializer(serializers.ModelSerializer):
    uid = serializers.PrimaryKeyRelatedField(queryset=Vtuber.objects.all())
    class Meta:
        model = On_Live
        fields = ('uid', 'live_title', 'live_url')#, 'start_time'

#2020-12-28 reminder
class ReminderSerializer(serializers.ModelSerializer):
    uid = VtuberSerializer()
    class Meta:
        model = Reminds
        fields = ('uid', 'start_datetime', 'live_title', 'live_url', 'audience')

class Reminder_POST_Serializer(serializers.ModelSerializer):
    uid = serializers.PrimaryKeyRelatedField(queryset=Vtuber.objects.all())
    class Meta:
        model = Reminds
        fields = ('uid', 'start_datetime', 'live_title', 'live_url', 'audience')#, 'start_time' ['uid', 'start_datetime', 'live_title', 'live_url', 'audience']