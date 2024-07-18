from rest_framework import serializers

from core.models import Lunch, LunchReport, User


class LunchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lunch
        fields = ['id', 'menu', 'user', 'day']


class LunchReportSerializer(serializers.ModelSerializer):
    lunch_id = serializers.IntegerField(source='lunch.id')

    class Meta:
        model = LunchReport
        fields = ['lunch_id', 'date', 'count']
