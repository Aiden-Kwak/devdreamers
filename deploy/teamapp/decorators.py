
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from teamapp.models import Team


def team_ownership_required(func):
    def decorated(request, *args, **kwargs):
        team = get_object_or_404(Team, pk=kwargs['pk'])
        if not team.writer == request.user:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return decorated

def team_is_visible(func):
    def decorated(request, *args, **kwargs):
        team = get_object_or_404(Team, pk=kwargs['pk'])
        if request.user.school == team.writer.school or team.to_open:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseNotFound()
    return decorated