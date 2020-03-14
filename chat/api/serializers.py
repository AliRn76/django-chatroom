

from django.contrib.auth.models import User

from rest_framework import serializers

from chat.models import Chat


class ChatSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_username')
    class Meta:
        model = Chat
        fields = ['user', 'message', 'datetime', 'image']

    def get_username(self, obj):
        username = obj.user.username
        return username
