from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import DeleteView, CreateView
from django.views.generic.base import View

from notificationapp.models import Notification, AdminNotification, ContestNotification
from teamapp.models import Team

#댓글알림 리다이렉트
class TeamCommentNotification(View):
    def get(self, request, notification_pk, post_pk, *arg, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        post = Team.objects.get(pk=post_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('/teams/comment/<int:pk>/', pk=post_pk)

#댓글알림 사용자확인
class NotificationCheckView(View):
    def post(self, request, *args, **kwargs):
        for notification in Notification.objects.filter(to_user=request.user, user_has_seen=False):
            notification.user_has_seen = True
            notification.save()
        # 전체공지 사용자확인
        for notification in AdminNotification.objects.filter(to_user=request.user, user_has_seen=False):
            notification.user_has_seen = True
            notification.save()

        return HttpResponse('Success', content_type='text/plain')

#댓글알림삭제
class NotificationDeleteView(View):
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)

        notification.user_has_seen = True
        notification.delete()

        return HttpResponse('Success', content_type='text/plain')

#댓글알림 전체삭제
class NotificationTotalDeleteView(View):
    def delete(self, request, notification_pk, *args, **kwargs):
        # for notification in Notification.objects.filter(to_user=request.user):
        #     notification = notification.objects.get(pk=notification_pk)
        #     notification.delete()
        Notification.objects.filter(to_user=request.user).get(pk=notification_pk).delete()

        return HttpResponse('Success', content_type='text/plain')

#공모전 알림
class ContestNotificationDeleteView(View):
    def delete(self, request, *args, **kwargs):
        for notification in ContestNotification.objects.filter(to_user=request.user, user_has_seen=False):
            notification.user_has_seen = True
            notification.delete()

        return HttpResponse('Success', content_type='text/plain')


#전체공지
class AnnouncementDeleteView(View):
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = AdminNotification.objects.get(pk=notification_pk)

        notification.user_has_seen = True
        notification.delete()

        return HttpResponse('Success', content_type='text/plain')






