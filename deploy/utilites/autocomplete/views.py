from django.http import JsonResponse
from django.views import View

from accountapp.models import Interest, Stack


class AutoCompleteInterest(View):
    def get(self, request):
        result = list(Interest.objects.all().values_list('name', flat=True).distinct())

        return JsonResponse({'data': result})


class AutoCompleteStack(View):
    def get(self, request):
        # data = request.GET.get("val", None)
        # result = None
        # if data:
        result = list(Stack.objects.all().values_list('name', flat=True).distinct())
        return JsonResponse({'data': result})