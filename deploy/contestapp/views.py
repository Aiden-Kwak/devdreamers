from datetime import datetime
from functools import reduce
from operator import or_

from django.db.models.query_utils import Q
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from commentapp.forms import ContestCommentCreationForm
from commentapp.models import ContestComment
from contestapp.forms import ContestCreationForm
from contestapp.models import Contest
from subscribeapp.models import ContestSubscription


class ContestListView(View):

    def get(self, request):
        offset = int(request.GET.get("offset", 0))
        title = request.GET.get("title", None)
        host = request.GET.get("host", None)
        category = request.GET.getlist("category[]", None)
        checked = int(request.GET.get("checked", 0))

        user = request.user
        subscription = None
        limit = 8

        Contest.objects.filter(finish_date__lt=datetime.now()).update(visible=False)

        if checked:
            contest_list = Contest.objects.order_by('-start_date').distinct() # 체크시 마감일기준x -> 등록일로 변경
        else:
            contest_list = Contest.objects.order_by('-finish_date').distinct() # 미체크시 등록일기준x -> 마감일로 변경

        poster_list = Contest.objects.order_by('-created_at').distinct() # 생성일 기준 포스터 5개 가져오기
        poster_list = poster_list[:8]

        if title:
            contest_list = contest_list.filter(title__contains=title).distinct()

        if host:
            contest_list = contest_list.filter(host__contains=host).distinct()

        if category:
            contest_list = contest_list.filter(reduce(or_, [Q(category__contains=q) for q in category])).distinct()

        if user.is_authenticated:
            subscription = list(ContestSubscription.objects.filter(user=user).values_list('contest', flat=True).distinct())

        contest_list = contest_list[offset:offset + limit]
        
        if request.is_ajax():
            num = contest_list.count()
            is_end = False
            if num < limit:
                is_end = True
            data = render_to_string('contestapp/snippets/contest_card.html', {'contest_list': contest_list, 'subscription': subscription, 'poster_list': poster_list})
            return JsonResponse({'data': data, 'is_end': is_end})

        else:
            return render(request, 'contestapp/page/contest_list.html', {"contest_list": contest_list, 'subscription': subscription, 'poster_list': poster_list})





class ContestCreateView(CreateView):
    model = Contest
    form_class = ContestCreationForm # 만들기
    template_name = 'contestapp/page/create.html'

    def form_valid(self, form):
        temp_contest = form.save(commit=False)
        temp_contest.writer = self.request.user
        temp_contest.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('contest:detail', kwargs={'pk':self.object.pk})


class ContestUpdateView(UpdateView):
    model = Contest
    context_object_name = 'target_contest'
    form_class = ContestCreationForm
    template_name = 'contestapp/page/update.html'


    def get_success_url(self):
        return reverse('contest:detail', kwargs={'pk': self.object.pk})


class ContestDeleteView(DeleteView):
    model = Contest
    context_object_name = 'target_contest'
    success_url = reverse_lazy('contest:list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ContestDetailView(DetailView):
    model = Contest
    context_object_name = 'target_contest'
    template_name = 'contestapp/page/detail.html'

    def get_context_data(self, **kwargs):
        contest = self.object
        user = self.request.user
        comment = ContestComment.objects.filter(contest=contest).count()

        if Contest.objects.all().count()==1:
            subscription = None
            if user.is_authenticated:
                subscription = ContestSubscription.objects.filter(user=user, contest=contest)
            return super(ContestDetailView, self).get_context_data(comment=comment, subscription=subscription, **kwargs)

        else:
            try:
                the_prev = Contest.objects.filter(pk__lt=contest.pk).order_by('-pk').first().pk
            except:
                the_prev = Contest.objects.filter(pk__gt=contest.pk).order_by('-pk').first().pk
            try:
                the_next = Contest.objects.filter(pk__gt=contest.pk).order_by('pk').first().pk
            except:
                the_next = Contest.objects.filter(pk__lt=contest.pk).order_by('pk').first().pk

            subscription = None
            if user.is_authenticated:
                subscription = ContestSubscription.objects.filter(user=user, contest=contest)
            return super(ContestDetailView, self).get_context_data(comment=comment, the_prev=the_prev, the_next=the_next, subscription = subscription, **kwargs)


class ContestCommentView(View):

    def get(self, request, pk):
        contest = get_object_or_404(Contest, pk=pk)
        comment_form = ContestCommentCreationForm()
        return render(request, 'contestapp/page/comment.html', {'pk':pk, 'form':comment_form, 'contest': contest})