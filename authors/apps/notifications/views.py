from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from .serializer import UserNotificationSerializer
from .models import UserNotification, NotificationSetting


class UserNotificationview(APIView):
    """Class For user to see all notifications."""
    queryset = UserNotification.objects.all()
    serializer_class = UserNotificationSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, **kwargs):
        """Gets all notifications."""
        user = request.user.username
        notifications = UserNotification.objects.filter(reciever=user)
        serializer = UserNotificationSerializer(notifications, many=True)
        return Response({"notifications": serializer.data}, status.HTTP_200_OK)


class GetNotification(APIView):
    """Class to get a specific notificatiom"""
    queryset = UserNotification.objects.all()
    serializer_class = UserNotificationSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self, id):
        try:
            return UserNotification.objects.get(id=id)
        except UserNotification.DoesNotExist:
            raise NotFound("Notification does not exists")

    def get(self, request, **kwargs):
        """Gets specific notification."""
        user = request.user.username
        notification = self.get_object(id=kwargs['id'])
        single_notification = UserNotification.objects.filter(reciever=user, id=kwargs['id'])
        if single_notification:
            single_notification.update(read=True)
            serializer = UserNotificationSerializer(single_notification,
                                                    many=True)
            return Response({"notification": serializer.data},
                            status=status.HTTP_200_OK)


class UpdateNotificationSettingView(APIView):
    """ Class to configure turning  off notifications."""
    queryset = NotificationSetting.objects.all()
    permission_classes = (IsAuthenticated, )

    def post(self, request, **kwargs):
        """Function updates."""
        user = request.user.username
        notification_setting = NotificationSetting.objects.filter(user=user)
        for notifer in notification_setting:
            if notifer.get_notification is True:
                notifer.get_notification = False
                notifer.save()
                return Response({"message": "You have sucessfully turned notifications off"},
                                status=status.HTTP_200_OK)
            elif notifer.get_notification is False:
                notifer.get_notification = True
                notifer.save()
                return Response({"message": "You have sucessfully turned notifications on"},
                                status=status.HTTP_200_OK)
