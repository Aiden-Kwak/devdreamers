from datetime import *

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string, get_template
from django.views.generic.base import View
from chatapp.models import LandingChat



class ChatView(View):

    def get(self, request):
        message = LandingChat.objects.all().order_by('date')
        return render(request, 'chatapp/landing_chat.html', {'message': message})


    def post(self, request):
        if request.is_ajax():
            #데이터 아무것도 없으면 받아오는 결과값이 없어 dbTrigger error발생할것
            if LandingChat.objects.all().count()==0:
                now = datetime.now()
                dbtrigger = int(request.POST.get('dbtrigger', 0))
                if not (dbtrigger):
                    model = LandingChat()
                    model.chat = request.POST.get('message')
                    model.writer = request.user
                    model.save()

                return JsonResponse({'last_msg': now, 'checkFirstChat': 1})
            #챗데이터가 이미 존재하는경우
            else:
                dbtrigger = int(request.POST.get('dbtrigger', 0))
                if (dbtrigger):
                    model = LandingChat()
                    last_msg = LandingChat.objects.latest('date').date
                    return JsonResponse({'message': model.chat, 'last_msg': last_msg, 'checkFirstChat': 0})
                else:
                    model = LandingChat()
                    model.chat = request.POST.get('message')
                    model.writer = request.user
                    model.save()
                    if LandingChat.objects.all().count()>50:
                        LandingChat.objects.earliest('date').delete()
                    last_msg = LandingChat.objects.latest('date').date
                    return JsonResponse({'message': model.chat, 'last_msg': last_msg})


