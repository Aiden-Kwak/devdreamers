from django.urls import path

from commentapp.views import CreateTeamCommentView, DeleteTeamCommentView, CreateContestCommentView, DeleteContestCommentView

app_name = 'comment'

urlpatterns = [
    path('team/<int:pk>/', CreateTeamCommentView.as_view(), name='team'),
    path('team/delete/', DeleteTeamCommentView.as_view(), name='team_delete'),
    path('contest/<int:pk>/', CreateContestCommentView.as_view(), name='contest'),
    path('contest/delete/', DeleteContestCommentView.as_view(), name='contest_delete'),

]