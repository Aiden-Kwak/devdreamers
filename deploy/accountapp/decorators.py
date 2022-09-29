from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy

from accountapp.models import Profile


def has_logined(func):
    def decorated(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('account:index'))
        return func(request, *args, **kwargs)
    return decorated

def has_profile(func):
    def decorated(request, *args, **kwargs):
        try:
            profile = request.user.profile
        except:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('account:index'))
    return decorated

def has_entered_create2(func):
    def decorated(request, *args, **kwargs):
        if request.user.profile.has_entered:
            return HttpResponseRedirect(reverse('account:index'))
        return func(request, *args, **kwargs)
    return decorated

def profile_is_visible(func):
    def decorated(request, *args, **kwargs):
        profile = get_object_or_404(Profile, nickname=kwargs['slug'])
        if request.user.school == profile.user.school or profile.to_open:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseNotFound()
    return decorated