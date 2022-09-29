from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Create your views here.
from django.views import View

from contestapp.models import Contest
from subscribeapp.models import TeamSubscription, ContestSubscription
from teamapp.models import Team


class TeamSubscriptionView(View):

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            pk = int(request.POST.get('pk', None))
            team = get_object_or_404(Team, pk=pk)
        # if team.to_open or user.school == team.writer.school:
            subscription = TeamSubscription.objects.filter(user=user, team=team)

            if pk:
                if subscription.exists():
                    subscription.delete()
                    return JsonResponse({'res': 0})
                else:
                    TeamSubscription(user=user, team=team).save()
                    return JsonResponse({'res': 1})

            else:
                response = JsonResponse({"message": "잘못된 접근입니다!"})
                response.status_code = 403
                return response
        else:
            response = JsonResponse({"message": "로그인 후 이용할 수 있습니다!"})
            response.status_code = 403
            return response

class ContestSubscriptionView(View):

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            pk = int(request.POST.get('pk', None))
            contest = get_object_or_404(Contest, pk=pk)
            subscription = ContestSubscription.objects.filter(user=user, contest=contest)

            if pk:
                if subscription.exists():
                    subscription.delete()
                    return JsonResponse({'res': 0})
                else:
                    ContestSubscription(user=user, contest=contest).save()
                    return JsonResponse({'res': 1})

            else:
                response = JsonResponse({"message": "잘못된 접근입니다!"})
                response.status_code = 403
                return response
        else:
            response = JsonResponse({"message": "로그인 후 이용할 수 있습니다!"})
            response.status_code = 403
            return response

