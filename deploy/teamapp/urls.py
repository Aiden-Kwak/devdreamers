from django.urls import path

from teamapp import views
from teamapp.views import TeamListView, TeamCreateView, TeamDetailView, TeamUpdateView, TeamDeleteView, TeamCommentView, \
    TeamCloseView

app_name = 'team'

urlpatterns = [
    path('', TeamListView.as_view(), name='list'),
    path('create/', TeamCreateView.as_view(), name='create'),
    path('<int:pk>/', TeamDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', TeamUpdateView.as_view(),name='update'),
    path('delete/<int:pk>/', TeamDeleteView.as_view(), name='delete'),
    path('comment/<int:pk>/', TeamCommentView.as_view(), name='comment'),
    path('close/<int:pk>/', TeamCloseView.as_view(), name='close')
]

