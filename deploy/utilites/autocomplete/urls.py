from django.urls import path

from utilites.autocomplete.views import AutoCompleteStack, AutoCompleteInterest

urlpatterns = [
    path('interest/', AutoCompleteInterest.as_view()),
    path('stack/', AutoCompleteStack.as_view()),
]

