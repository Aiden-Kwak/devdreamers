"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('markdownx/', include('markdownx.urls')),
    path('', include('accountapp.urls')),
    path('teams/', include('teamapp.urls')),
    path('subscribe/', include('subscribeapp.urls')),
    path('comment/', include('commentapp.urls')),
    path('autocomplete/', include('utilites.autocomplete.urls')),
    path('contest/', include('contestapp.urls')),
    path('intro/', TemplateView.as_view(template_name='intro.html')),
    path('', include('notificationapp.urls')),
    path('chat/', include('chatapp.urls')),
    path('robots.txt/', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    path('sitemap.xml/', TemplateView.as_view(template_name="sitemap.xml", content_type='text/plain')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
