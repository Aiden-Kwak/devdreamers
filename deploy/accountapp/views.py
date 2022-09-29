import json


# Create your views here.
from datetime import datetime
from django.contrib.auth import get_user_model

from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404, resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from accountapp.decorators import has_logined, has_profile, has_entered_create2, profile_is_visible
from accountapp.forms import AccountCreateForm, ProfileCreationForm, ProfileUpdateForm, ResetNicknameForm, \
    ChangePasswordForm, ActivityForm, LanguageForm, CertificateForm, InternForm, AwardForm, \
    PasswordResetForm, SetPasswordForm
from accountapp.models import Profile, User, Interest, Stack
from accountapp.token import account_activation_token
from subscribeapp.models import TeamSubscription, ContestSubscription
from teamapp.models import Team
from contestapp.models import Contest

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

User = get_user_model()
INTERNAL_RESET_URL_TOKEN = 'set-password'
INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'



class IndexTemplateView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            school = request.user.school

            Team.objects.filter(deadline__lt=datetime.now()).update(visible=False)
            team_subscription = list(TeamSubscription.objects.filter(user=user).values_list('team', flat=True).distinct())

            # team_list = Team.objects.filter(to_open=True, visible=True).order_by('-created_at')[:10]
            # profile_list = Profile.objects.filter(to_open=True).order_by('-created_at')[:10]
            team_list = Team.objects.filter((Q(to_open=True) | Q(writer__school=school)), Q(visible=True)).order_by('-created_at')[:10]
            profile_list = Profile.objects.filter((Q(to_open=True) | Q(user__school=school))).order_by('-created_at')[:10]

            return render(request, 'index/index.html', {'team_list': team_list, 'profile_list': profile_list, 'team_subscription': team_subscription})
        else:
            team_list = Team.objects.filter(to_open=True, visible=True).order_by('-created_at')[:10]
            profile_list = Profile.objects.filter(to_open=True).order_by('-created_at')[:10]
            team_subscription = None
            return render(request, 'index/index.html', {'team_list': team_list, 'profile_list': profile_list, 'team_subscription': team_subscription})

class SettingTemplateView(View):
    def get(self, request):
        user = request.user

        profile = Profile.objects.get(user=user)
        image = profile.image
        nickname = profile.nickname

        return render(request, 'index/setting.html', {'image': image, 'nickname': nickname})


class Activate(View):
    def get(self, request, uid64, token):
        uid = force_text(urlsafe_base64_decode(uid64))
        user = User.objects.get(pk=uid)

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'accountapp/email/authenticate_email.html')

        else:
            return HttpResponseNotFound()


@method_decorator(has_logined, 'get')
@method_decorator(has_logined, 'post')
class AccountCreateView(View):
    def get(self, request):
        form = AccountCreateForm()
        return render(request, 'accountapp/page/auth/signup.html', {'form':form})

    def post(self, request):
        form = AccountCreateForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                temp_user = form.save(commit=False)
                temp_user.is_active = False
                temp_user.save()
                current_site = get_current_site(request=self.request)

                message = render_to_string('accountapp/email/validation_email.html', {
                    'user': temp_user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(temp_user.pk)).encode().decode(),
                    'token': account_activation_token.make_token(temp_user),
                })

                mail_subject = "[꿈꾸는 개발자들] 회원가입 인증 메일입니다."
                user_email = temp_user.email
                email = EmailMessage(subject=mail_subject, body=message, to=[user_email])
                email.content_subtype = 'html'
                email.send()

            html = render_to_string('accountapp/email/send_email.html')

            return JsonResponse({'html': html})
        else:
            # Error 메시지 보내기
            errors = [(k, v[0]) for k, v in form.errors.items()]
            return JsonResponse({'message': errors})


class AccountDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('account:index')
    template_name = 'accountapp/page/auth/quit.html'

    def get_object(self):
        return self.request.user


class ChangePasswordView(UpdateView):
    model = User
    form_class = ChangePasswordForm
    template_name = 'accountapp/page/auth/reset_password.html'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()

        return render(self.request,'accountapp/snippets/setting_success.html')


class FindIDView(View):
    def get(self, request):
        return render(self.request, 'accountapp/page/auth/find_id.html')

    def post(self, request):
        current_site = get_current_site(request=self.request)
        user_email = self.request.POST.get('email')
        user = get_object_or_404(User.objects, email = user_email)
        if user is not None:
            mail_subject = "[꿈꾸는 개발자들] 아이디 찾기 메일입니다."
            message = render_to_string('accountapp/email/validation_email_find_id.html', {
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
            })
            email = EmailMessage(subject=mail_subject, body=message, to=[user_email])
            email.content_subtype = 'html'
            email.send(fail_silently=False)

            html = render_to_string('accountapp/email/send_email.html')
            return JsonResponse({'html': html})

class FindIDVerifiedView(View):
    def get(self, request, uid64):
        uid = force_text(urlsafe_base64_decode(uid64))
        user = User.objects.get(pk=uid)
        
        return render(request, 'accountapp/page/auth/found_id.html', context={'id': user.username})


class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context

class FindPWView(PasswordContextMixin, FormView):
    form_class = PasswordResetForm
    title = _('Password reset')

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get(self, request):
        return render(self.request, 'accountapp/page/auth/find_pw.html')

    def form_valid(self, form):
        current_site = get_current_site(request=self.request)
        user_email = self.request.POST.get('email')
        user_id = self.request.POST.get('id')
        user = get_object_or_404(User.objects, email = user_email) 
        if user is not None:
            if user.username == user_id:
                mail_subject = "[꿈꾸는 개발자들] 비밀번호 재설정 메일입니다."
                message = render_to_string('accountapp/email/validation_email_find_pw.html', {
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
                    'token': default_token_generator.make_token(user)
                })
                email = EmailMessage(subject=mail_subject, body=message, to=[user_email])
                email.content_subtype = 'html'
                email.send(fail_silently=False)
                
                html = render_to_string('accountapp/email/send_email.html')
                return JsonResponse({'html': html})
                

class FindPWVerifiedView(PasswordResetConfirmView): 
    template_name = 'accountapp/page/auth/find_pw_verified.html'
    success_url = reverse_lazy('account:findpwcomplete')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if token == self.reset_url_token:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, self.reset_url_token)
                    return HttpResponseRedirect(redirect_url)

        return render(self.request, '404.html')


class FindPWCompleteView(PasswordContextMixin, TemplateView):
    template_name = 'accountapp/page/auth/find_pw_complete.html'
    title = _('Password reset complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(reverse_lazy('account:login'))
        return context


@method_decorator(has_profile, 'get')
@method_decorator(has_profile, 'post')
class ProfileCreateView(CreateView):
    model = Profile
    form_class = ProfileCreationForm
    success_url = reverse_lazy('account:create2')
    template_name = 'accountapp/page/profile/create/create.html'

    def form_valid(self, form):
        temp_profile = form.save(commit=False)
        temp_profile.user = self.request.user
        temp_profile.save()
        return super().form_valid(form)


class UpdateNicknameView(UpdateView):
    model = User
    form_class = ResetNicknameForm
    template_name = 'accountapp/page/profile/update/update_nickname.html'

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super(UpdateNicknameView, self).get_context_data(**kwargs)
        context['nickname'] = Profile.objects.get(user=self.request.user).nickname

        return context

    def form_valid(self, form):
        form.save()
        nickname = form.cleaned_data['nickname']

        return render(self.request,'accountapp/snippets/setting_success.html', {'nickname': nickname})

class ProfileDetailView(View):

    def get(self, request, slug):
        profile = get_object_or_404(Profile, nickname= slug)
        user = profile.user
        visible = True
        # visible = False
        # if request.user.school == profile.user.school or profile.to_open:
        #     visible = True
        return render(request,'accountapp/page/profile/detail/detail.html', {'user' : user, 'visible':visible})

    def post(self, request, slug):
        profile = get_object_or_404(Profile, nickname= slug)
        profile.self_intro = request.POST.get('self_intro')
        profile.save()
        return JsonResponse({'self_intro': profile.self_intro})

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        context['self_intro'] = Profile.objects.get(user=self.request.user).self_intro

        return context

# @method_decorator(profile_is_visible, 'get')
class ProfileArticleView(View):

    def get(self, request, slug):
        cur_profile = get_object_or_404(Profile, nickname=slug)
        cur_user = cur_profile.user
        user = request.user

        team_subscription = list(TeamSubscription.objects.filter(user=user).values_list('team', flat=True).distinct())

        if request.user == cur_user:
            team_list = cur_user.team.all().order_by('-created_at')
        else:
            # team_list = Team.objects.filter(to_open=True, writer=cur_user).order_by('-created_at')
            team_list = Team.objects.filter(Q(to_open=True)|Q(writer__school=request.user.school), writer=cur_user).order_by('-created_at')

        return render(request,'accountapp/page/profile/detail/article.html', {'user':cur_user, 'team_list':team_list, 'team_subscription': team_subscription})

class ProfileSubscribeView(View):

    def get(self, request):
        user = request.user

        team_subscription = list(TeamSubscription.objects.filter(user=user).values_list('team', flat=True).distinct())
        contest_subscription = list(ContestSubscription.objects.filter(user=user).values_list('contest', flat=True).distinct())

        team = TeamSubscription.objects.filter(user=user).values_list('team')
        team_list = Team.objects.filter(id__in=team).order_by('-updated_at')

        contest = ContestSubscription.objects.filter(user=user).values_list('contest')
        contest_list = Contest.objects.filter(id__in=contest).order_by('-created_at')
        
        return render(request, 'accountapp/page/profile/detail/subscribe.html', {'team_list':team_list, 'team_subscription':team_subscription, 'contest_list':contest_list, 'subscription':contest_subscription})


class ProfileListView(View):

    def get(self, request):
        offset = int(request.GET.get("offset", 0))
        interest = request.GET.get("interest", None)
        stack = request.GET.get("stack", None)
        status = request.GET.getlist("status[]", None)
        type = request.GET.getlist("type[]", None)

        user = request.user
        school = None
        if user.is_authenticated:
            school = user.school
        limit = 21

        # profile_list = Profile.objects.filter(to_open=True).order_by('-updated_at').distinct()
        profile_list = Profile.objects.filter((Q(to_open=True) | Q(user__school=school))).order_by('-updated_at').distinct()

        if stack:
            stack = stack.strip().split(',')
            profile_list = profile_list.filter(stack__name__in=stack).distinct()

        if interest:
            interest = interest.strip().split(',')
            profile_list = profile_list.filter(interest__name__in=interest).distinct()

        if status:
            profile_list = profile_list.filter(status__in=status).distinct()

        if type:
            profile_list = profile_list.filter(type__in=type).distinct()

        profile_list = profile_list[offset:offset+limit]

        if request.is_ajax():
            num = profile_list.count()
            is_end = False
            if num < limit:
                is_end = True
            data = render_to_string('accountapp/snippets/card.html', {'profile_list': profile_list})
            return JsonResponse({'data': data, 'is_end': is_end})

        else:
            return render(request, 'accountapp/page/profile/list/list.html', {"profile_list": profile_list})


@method_decorator(has_entered_create2, 'get')
@method_decorator(has_entered_create2, 'post')
class ProfileExtraCreateView(View):

    def get(self, request):

        return render(request, 'accountapp/page/profile/create/create2.html')

    def post(self, request):
        profile = request.user.profile
        activity_num = int(request.POST.get('activity_num', 0))
        lang_num = int(request.POST.get('lang_num', 0))
        cert_num = int(request.POST.get('cert_num', 0))
        award_num = int(request.POST.get('award_num', 0))
        intern_num = int(request.POST.get('intern_num', 0))

        activity_form = ActivityForm(request.POST, instance=profile, num= activity_num)
        language_form = LanguageForm(request.POST, instance=profile, num= lang_num)
        certificate_form = CertificateForm(request.POST, instance=profile, num= cert_num)
        award_form = AwardForm(request.POST, instance=profile, num= award_num)
        intern_form = InternForm(request.POST, instance=profile, num= intern_num)

        if activity_form.is_valid():
            activity_form.save()
        if language_form.is_valid():
            language_form.save()
        if certificate_form.is_valid():
            certificate_form.save()
        if award_form.is_valid():
            award_form.save()
        if intern_form.is_valid():
            intern_form.save()

        profile.type = request.POST.get('profile_type', '0')
        profile.status = request.POST.get('current_status', '0')

        profile.save()

        interest = request.POST.get('interest', None)
        stack = request.POST.get('stack', None)
        profile.interest.clear()
        profile.stack.clear()

        if interest:
            interest = interest.strip()
            interest = interest.split(',')

            for i in interest:
                name = i.strip()
                if name:
                    tag, is_tag_created = Interest.objects.get_or_create(name=name)
                    profile.interest.add(tag)

        if stack:
            stack = stack.strip()
            stack = stack.split(',')

            for s in stack:
                name = s.strip()
                if name:
                    tag, is_tag_created = Stack.objects.get_or_create(name=name)
                    profile.stack.add(tag)

        profile.has_entered = True
        profile.save()

        return HttpResponseRedirect(reverse_lazy('account:index'))


class ProfileUpdateView(View):

    def get(self, request):

        profile = Profile.objects.get(user=request.user)

        interest = list(profile.interest.values_list('name', flat=True).distinct())
        stack = list(profile.stack.values_list('name', flat=True).distinct())

        interest = ','.join(interest)
        stack = ','.join(stack)

        return render(request, 'accountapp/page/profile/update/update.html', context={'profile': profile, 'interest': interest,'stack': stack})

    def post(self, request):
        profile = request.user.profile
        school_status = request.POST.get('school_status', '0')
        activity_num = int(request.POST.get('activity_num', 0))
        lang_num = int(request.POST.get('lang_num', 0))
        cert_num = int(request.POST.get('cert_num', 0))
        award_num = int(request.POST.get('award_num', 0))
        intern_num = int(request.POST.get('intern_num', 0))

        profile_form = ProfileUpdateForm(request.POST, request.FILES)
        activity_form = ActivityForm(request.POST, instance=profile, num= activity_num)
        language_form = LanguageForm(request.POST, instance=profile, num= lang_num)
        certificate_form = CertificateForm(request.POST, instance=profile, num= cert_num)
        award_form = AwardForm(request.POST, instance=profile, num= award_num)
        intern_form = InternForm(request.POST, instance=profile, num= intern_num)

        if profile_form.is_valid():
            if profile_form.cleaned_data['image'] != profile_form.fields['image'].initial:
                profile.image = profile_form.cleaned_data['image']
            profile.email = profile_form.cleaned_data['email']
            profile.github = profile_form.cleaned_data['github']
            profile.status = profile_form.cleaned_data['status']
            profile.type = profile_form.cleaned_data['type']
            profile.to_open = profile_form.cleaned_data['to_open']
            profile.save()

        if activity_form.is_valid():
            activity_form.save()
        if language_form.is_valid():
            language_form.save()
        if certificate_form.is_valid():
            certificate_form.save()
        if award_form.is_valid():
            award_form.save()
        if intern_form.is_valid():
            intern_form.save()

        profile.user.school_status = school_status
        profile.user.save()

        interest = request.POST.get('interest', None)
        stack = request.POST.get('stack', None)
        profile.interest.clear()
        profile.stack.clear()

        if interest:
            interest = interest.strip()
            interest = interest.split(',')

            for i in interest:
                name = i.strip()
                if name:
                    tag, is_tag_created = Interest.objects.get_or_create(name=name)
                    profile.interest.add(tag)

        if stack:
            stack = stack.strip()
            stack = stack.split(',')
            for s in stack:
                name = s.strip()
                if name:
                    tag, is_tag_created = Stack.objects.get_or_create(name=name)
                    profile.stack.add(tag)

        return render(request, 'accountapp/page/profile/detail/detail.html', context={'slug': request.user.profile.nickname, 'form':profile_form, 'visible':True})

