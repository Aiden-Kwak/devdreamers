from django.urls import path

from chatapp.views import ChatView

app_name = 'chatapp'

urlpatterns = [
    path('', ChatView.as_view(), name='landing-chat'),
    # path('', ChatRenderView.as_view(), name='landing-chat-msg')
]