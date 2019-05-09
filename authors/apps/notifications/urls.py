from django.urls import path
from .views import UserNotificationview, UpdateNotificationSettingView, GetNotification


urlpatterns = [
     path('notifications/', UserNotificationview.as_view(),
          name='notifications'),
     path('notifications/<id>/', GetNotification.as_view(),
          name='notifications_id'),
     path('notification/settings/', UpdateNotificationSettingView.as_view(),
          name='set_notifications')
]
