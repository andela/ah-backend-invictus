from rest_framework import serializers
from authors.apps.notifications.models import UserNotification


class UserNotificationSerializer(serializers.ModelSerializer):
    """ serializers for notifications"""

    class Meta:
        model = UserNotification
        fields = ('id', 'created_at', 'message', 'reciever', 'link', 'read')
