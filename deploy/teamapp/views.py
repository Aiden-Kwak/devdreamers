from datetime import datetime
from functools import reduce
from operator import or_

from django.db.models import Q

# Create your views here.
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from commentapp.forms import TeamCommentCreationForm
from subscribeapp.models import TeamSubscription
from teamapp.decorators import team_ownership_required, team_is_visible
from teamapp.forms import TeamCreationForm
from teamapp.models import Team



class TeamListView(View):

    def get(self, request):
        offset = int(request.GET.get("offset", 0))
        title = request.GET.get("title", None)
        nickname = request.GET.get("nickname", None)
        category = request.GET.getlist("category[]", None)
        type = request.GET.getlist("type[]", None)

        user = request.user
        subscription = None
        school = None
        if user.is_authenticated:
            school = user.school
        limit = 12

        Team.objects.filter(deadline__lt=datetime.now()).update(visible=False)

        team_list = Team.objects.filter(Q(to_open=True) | Q(writer__school=school)).order_by('-updated_at').distinct()
        # team_list = Team.objects.filter(to_open=True).order_by('-updated_at').distinct()

        if title:
            team_list = team_list.filter(title__contains=title).distinct()

        if nickname:
            team_list = team_list.filter(writer__profile__nickname__contains=nickname).distinct()

        if type:
            team_list = team_list.filter(type__in=type).distinct()

        if category:
            team_list = team_list.filter(reduce(or_, [Q(category__contains=q) for q in category])).distinct()

        if user.is_authenticated:
            subscription = list(TeamSubscription.objects.filter(user=user).values_list('team', flat=True).distinct())

        team_list = team_list[offset:offset+limit]

        if request.is_ajax():
            num = team_list.count()
            is_end = False
            if num < limit:
                is_end = True
            data = render_to_string('teamapp/snippets/card.html', {'team_list': team_list, 'team_subscription': subscription})
            return JsonResponse({'data': data, 'is_end': is_end})

        else:
            return render(request, 'teamapp/page/list.html', {"team_list": team_list, 'team_subscription': subscription})


class TeamCreateView(CreateView):
    model = Team
    form_class = TeamCreationForm # 만들기
    template_name = 'teamapp/page/create.html'

    def form_valid(self, form):
        temp_team = form.save(commit=False)
        temp_team.writer = self.request.user
        temp_team.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('team:detail', kwargs={'pk':self.object.pk})

@method_decorator(team_ownership_required, 'get')
@method_decorator(team_ownership_required, 'post')
class TeamUpdateView(UpdateView):
    model = Team
    context_object_name = 'target_team'
    form_class = TeamCreationForm
    template_name = 'teamapp/page/update.html'


    def get_success_url(self):
        return reverse('team:detail', kwargs={'pk': self.object.pk})

    def get(self, request, *args, **kwargs):
         self.object = self.get_object() #오브젝트받고 -> 폼클래스 받고 -> 리턴
         form_class = self.get_form_class()
         form = self.get_form(form_class)
         context = self.get_context_data(object=self.object, form=form)
         return self.render_to_response(context)


@method_decorator(team_ownership_required, 'get')
@method_decorator(team_ownership_required, 'post')
class TeamDeleteView(DeleteView):
    model = Team
    context_object_name = 'target_team'
    success_url = reverse_lazy('team:list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)



# @method_decorator(team_is_visible, 'get')
class TeamDetailView(DetailView):
    model = Team
    context_object_name = 'target_team'
    template_name = 'teamapp/page/detail.html'

    def get_context_data(self, **kwargs):
        team = self.object
        user = self.request.user
        school = None
        if user.is_authenticated:
            school = user.school
        team_list = Team.objects.filter(Q(to_open=True) | Q(writer__school=school))
        if Team.objects.all().count()==1:
            subscription = None
            if user.is_authenticated:
                subscription = TeamSubscription.objects.filter(user=user, team=team)
            return super(TeamDetailView, self).get_context_data(subscription=subscription, **kwargs)

        else:
            try:
                the_prev = team_list.filter(pk__lt=team.pk).order_by('-pk').first().pk
            except:
                the_prev = team_list.filter(pk__gt=team.pk).order_by('-pk').first().pk
            try:
                the_next = team_list.filter(pk__gt=team.pk).order_by('pk').first().pk
            except:
                the_next = team_list.filter(pk__lt=team.pk).order_by('pk').first().pk

            subscription = None
            if user.is_authenticated:
                subscription = TeamSubscription.objects.filter(user=user, team=team)
            return super(TeamDetailView, self).get_context_data(the_prev=the_prev, the_next=the_next, subscription = subscription, **kwargs)

# @method_decorator(team_is_visible, 'get')
class TeamCommentView(View):

    def get(self, request, pk):
        team = get_object_or_404(Team, pk=pk)
        comment_form = TeamCommentCreationForm()
        return render(request, 'teamapp/page/comment.html', {'pk':pk, 'form':comment_form, 'team': team})


class TeamCloseView(View):

    def get(self, request, pk):
        return HttpResponseRedirect(reverse_lazy('team:detail', kwargs={'pk': pk}))

    def post(self, request, pk):
        team = get_object_or_404(Team, pk=pk)

        if team.writer == request.user:
            team.visible = False
            team.save()

        return HttpResponseRedirect(reverse_lazy('team:detail', kwargs={'pk': pk}))


