from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from django.views.generic import TemplateView

from accountapp.views import AccountCreateView, AccountDeleteView, ProfileCreateView, \
    ProfileDetailView, ProfileListView, ProfileExtraCreateView, IndexTemplateView, Activate, ProfileUpdateView, \
    UpdateNicknameView, ChangePasswordView, SettingTemplateView, ProfileArticleView, ProfileSubscribeView, \
    FindIDView, FindIDVerifiedView, FindPWView, FindPWVerifiedView, FindPWCompleteView

app_name = 'account'

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('login/', LoginView.as_view(template_name='accountapp/page/auth/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', AccountCreateView.as_view(), name='signup'),
    path('findaccount/', LoginView.as_view(template_name='accountapp/page/auth/find_account.html', redirect_authenticated_user=True), name='findaccount'),
    path('findid/', FindIDView.as_view(), name='findid'),   
    path('findid/verified/<str:uid64>/', FindIDVerifiedView.as_view(), name='findidverified'), 
    path('findpw/', FindPWView.as_view(), name="findpw"),
    path('findpw/verified/<uidb64>/<token>/', FindPWVerifiedView.as_view(), name="findpwverified"),
    path('findpw/complete/', FindPWCompleteView.as_view(), name="findpwcomplete"),
    path('account/activate/<str:uid64>/<str:token>/', Activate.as_view(), name='activate'),
    path('settings/', SettingTemplateView.as_view(), name='setting'),
    path('profile/create/', ProfileCreateView.as_view(), name='create'),
    path('profile/create2/', ProfileExtraCreateView.as_view(), name='create2'),
    path('profile/update/', ProfileUpdateView.as_view(), name='update'),
    path('member/detail/<slug>/', ProfileDetailView.as_view(), name='detail'),
    path('member/article/<slug>/', ProfileArticleView.as_view(), name='article'),
    path('member/subscribe/', ProfileSubscribeView.as_view(), name='subscribe'),
    path('members/', ProfileListView.as_view(), name='list'),
    path('settings/reset-password/', ChangePasswordView.as_view(), name='setting_password'),
    path('settings/nickname/', UpdateNicknameView.as_view(), name='setting_nickname'),
    path('settings/quit/', AccountDeleteView.as_view(), name='delete'),
    path('note/', TemplateView.as_view(template_name="note.html"), name='note') # 임시 공지 html
]