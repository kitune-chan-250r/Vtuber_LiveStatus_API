from rest_framework import serializers
from .models import Vtuber, On_Live

class VtuberSerializer(serializers.ModelSerializer):
    production = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()

    class Meta:
        model = Vtuber
        fields = ('uid', 'liver_name', 'production', 'gender')

    def get_gender(self, obj):
        return obj.get_gender_display()

    def get_production(self, obj):
        return obj.get_production_display()

class OnLiveSerializer(serializers.ModelSerializer):
    uid = VtuberSerializer()
    class Meta:
        model = On_Live
        fields = ('uid', 'start_time', 'live_title')

