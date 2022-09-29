import re

from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.utils.http import is_safe_url


PROFILE_EXEMPT_URLS = [re.compile(url) for url in settings.PROFILE_EXEMPT_URLS]
LOGIN_EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
ADMIN_URLS = [re.compile(url) for url in settings.ADMIN_URLS]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    LOGIN_EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]


class CheckAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path_info.lstrip('/')
        access_admin = False
        if any(m.match(path) for m in ADMIN_URLS):
            access_admin = True

        if not request.user.is_authenticated:
            if not any(m.match(path) for m in LOGIN_EXEMPT_URLS):
                redirect_to = settings.LOGIN_URL
                # 'next' variable to support redirection to attempted page after login
                if len(path) > 0 and is_safe_url(
                    url = request.path_info, allowed_hosts=request.get_host()):
                    redirect_to = f"{settings.LOGIN_URL}?next={request.path_info}"

                return HttpResponseRedirect(redirect_to)

        else:
            if not any(m.match(path) for m in PROFILE_EXEMPT_URLS):
                try:
                    profile = request.user.profile.nickname
                except:
                    return HttpResponseRedirect(settings.PROFILE_CREATE_URL)
                else:
                    if access_admin:
                        if request.user.is_superuser and request.user.is_admin:
                            pass
                        else:
                            return HttpResponseRedirect(settings.INDEX_URL)

class NoteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not request.environ['PATH_INFO'] == "/note/":
            return HttpResponseRedirect(settings.NOTE_URL)
        return response

