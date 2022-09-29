from django import template

from notificationapp.models import Notification, ContestNotification, AdminNotification

register = template.Library()

@register.inclusion_tag('notificationapp/show_notifications.html', takes_context=True)
def show_notifications(context):
	request_user = context['request'].user
	# 댓글공지 context
	# notifications = Notification.objects.filter(to_user=request_user).exclude(user_has_seen=True).order_by('-date')
	notifications = Notification.objects.filter(to_user=request_user).order_by('-date')
	count_notifications = Notification.objects.filter(to_user=request_user, user_has_seen=False).count()
	no_notifications = Notification.objects.filter(to_user=request_user).count()

	#전체공지 context
	announcements = AdminNotification.objects.filter(to_user=request_user).order_by('-date')
	count_announcement = AdminNotification.objects.filter(to_user=request_user, user_has_seen=False).count()
	no_announcements = AdminNotification.objects.filter(to_user=request_user).count()

	#TOTAL COUNT
	noti_count = count_notifications + count_announcement
	no_notifications = no_notifications+no_announcements

	context = {
		'notifications': notifications,
		'noti_count': noti_count,
		'no_notifications': no_notifications,

		'announcements': announcements,
	}
	return context

@register.inclusion_tag('notificationapp/contest_notify.html', takes_context=True)
def contest_notifications(context):
	request_user = context['request'].user
	contest_notify = ContestNotification.objects.filter(to_user=request_user)

	return {'contest_notify': contest_notify, 'request': context['request']}
