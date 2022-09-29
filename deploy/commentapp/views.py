from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.\
from django.urls import reverse_lazy
from django.views import View
from commentapp.forms import TeamCommentCreationForm, ContestCommentCreationForm
from commentapp.models import TeamComment, ContestComment
from contestapp.models import Contest
from teamapp.models import Team


class CreateTeamCommentView(View):
    # def get(self, request, pk):
    #     return HttpResponseRedirect(reverse_lazy('team:comment', kwargs={'pk': pk}))

    def post(self, request, pk):
        team = get_object_or_404(Team, pk=pk)
        if request.user.is_authenticated:
            # if team.to_open or request.user.school == team.writer.school:
            comment_form = TeamCommentCreationForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.team = team
                comment.user = request.user
                comment.save()
                return JsonResponse({"message": "작성 완료"})

            else:
                response = JsonResponse({"message": "작성 실패했습니다."})
                response.status_code = 403
                return response
        else:
            response = JsonResponse({"message": "로그인 후 이용할 수 있습니다!"})
            response.status_code = 403
            return response

class DeleteTeamCommentView(View):
    def get(self, request, pk):
        comment = get_object_or_404(TeamComment, id=pk)
        team = comment.team
        return HttpResponseRedirect(reverse_lazy('team:comment', kwargs={'pk': team.id}))

    def post(self, request):
        if request.user.is_authenticated:
            pk = int(request.POST.get('pk', None))
            if pk:
                comment = get_object_or_404(TeamComment, id=pk)
                if comment.user == request.user:
                    comment.delete()
                    return JsonResponse({"message": "댓글 삭제 완료"})

                response = JsonResponse({"message": "잘못된 접근입니다!"})
                response.status_code = 403
                return response
            else:
                response = JsonResponse({"message": "잘못된 접근입니다!"})
                response.status_code = 403
                return response
        else:
            response = JsonResponse({"message": "로그인 후 이용할 수 있습니다!"})
            response.status_code = 403
            return response


class CreateContestCommentView(View):

    def post(self, request, pk):
        contest = get_object_or_404(Contest, pk=pk)
        if request.user.is_authenticated:
            comment_form = ContestCommentCreationForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.contest = contest
                comment.user = request.user
                comment.save()
                return JsonResponse({"message": "작성 완료"})

            else:
                response = JsonResponse({"message": "작성 실패했습니다."})
                response.status_code = 403
                return response
        else:
            response = JsonResponse({"message": "로그인 후 이용할 수 있습니다!"})
            response.status_code = 403
            return response

class DeleteContestCommentView(View):

    def get(self, request, pk):
        comment = get_object_or_404(ContestComment, id=pk)
        contest = comment.contest
        return HttpResponseRedirect(reverse_lazy('contest:comment', kwargs={'pk': contest.id}))

    def post(self, request):
        if request.user.is_authenticated:
            pk = int(request.POST.get('pk', None))
            if pk:
                comment = get_object_or_404(ContestComment, id=pk)
                if comment.user == request.user:
                    comment.delete()
                    return JsonResponse({"message": "댓글 삭제 완료"})

                response = JsonResponse({"message": "잘못된 접근입니다!"})
                response.status_code = 403
                return response
            else:
                response = JsonResponse({"message": "잘못된 접근입니다!"})
                response.status_code = 403
                return response
        else:
            response = JsonResponse({"message": "로그인 후 이용할 수 있습니다!"})
            response.status_code = 403
            return response

