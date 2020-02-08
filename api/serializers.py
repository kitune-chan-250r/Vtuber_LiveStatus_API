from rest_framework import serializers
from .models import Vtuber, On_Live

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
        fields = ('uid', 'start_time', 'live_title', 'live_url')