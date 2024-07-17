from core.models import Lunch, User
from django.shortcuts import get_object_or_404
from rest_framework import serializers


class LunchSerializer(serializers.ModelSerializer):
    # post_type_display = serializers.SerializerMethodField()
    # author_email = serializers.SerializerMethodField()
    # author_name = serializers.SerializerMethodField()

    class Meta:
        model = Lunch
        fields = ['id', 'menu', 'user', 'day']

    # def get_post_type_display(self, obj):
    #     return obj.get_post_type_display()
    #
    # def get_author_email(self, obj):
    #     author = get_object_or_404(User, id=obj.author_id)
    #     return author.email
    #
    # def get_author_name(self, obj):
    #     author = get_object_or_404(User, id=obj.author_id)
    #     return author.name
