from django.urls import path

from contestapp.views import ContestListView, ContestCreateView, ContestDetailView, ContestUpdateView, ContestDeleteView, ContestCommentView

app_name = 'contest'

urlpatterns = [
    path('', ContestListView.as_view(), name='list'),
    path('create/', ContestCreateView.as_view(), name='create'),
    path('<int:pk>/', ContestDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', ContestUpdateView.as_view(),name='update'),
    path('delete/<int:pk>/', ContestDeleteView.as_view(), name='delete'),
    path('comment/<int:pk>/', ContestCommentView.as_view(), name='comment'),
]