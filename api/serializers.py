from rest_framework import serializers
from .models import Vtuber, On_Live, ScheduledLive

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
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        fields = ('uid', 'live_title', 'live_url')#, 'start_time'
=======
=======
>>>>>>> Stashed changes
        fields = ('uid', 'start_time', 'live_title', 'live_url')


class ScheduledLiveSerializer(serializers.ModelSerializer):
    uid = VtuberSerializer()
    class Meta:
        model = ScheduledLive
        fields = ('uid', 'title', 'start_time', 'live_url')

class ScheduledLive_POST_Serializer(serializers.ModelSerializer):
    uid = serializers.PrimaryKeyRelatedField(queryset=Vtuber.objects.all())
    class Meta:
        model = ScheduledLive
        fields = ('uid', 'title', 'start_time', 'live_url')
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
