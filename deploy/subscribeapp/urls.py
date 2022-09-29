from django.urls import path

from subscribeapp.views import TeamSubscriptionView, ContestSubscriptionView

app_name = 'subscribe'

urlpatterns = [
    path('team/', TeamSubscriptionView.as_view(), name='team'),
    path('contest/', ContestSubscriptionView.as_view(), name='contest'),
]

