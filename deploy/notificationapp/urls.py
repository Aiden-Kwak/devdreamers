from django.urls import path

# from notificationapp.views import NotificationView
from notificationapp.views import TeamCommentNotification, NotificationDeleteView, NotificationCheckView, ContestNotificationDeleteView, AnnouncementDeleteView

app_name = 'notificationapp'

urlpatterns = [
    # path('', NotificationView.as_view(), name='show-notifications'),
    path('teams/comment/<int:post_pk>/', TeamCommentNotification.as_view(), name='post-notification'),
    path('notification/delete/<int:notification_pk>', NotificationDeleteView.as_view(), name='notification-delete'),
    path('notification/check/', NotificationCheckView.as_view(), name='notification-check'),
    path('notification/contest/check/', ContestNotificationDeleteView.as_view(), name='contest-notify-check'),
    path('notification/remove-all/<int:notification_pk>', NotificationDeleteView.as_view(), name='notification-remove-all'),
    path('announce/delete/<int:notification_pk>', AnnouncementDeleteView.as_view(), name='announcement-delete'),
]