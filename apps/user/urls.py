from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from user.views import LoginView, UserMainView, Test, PermissionMainView, RoleMainView, MainView
from user.views import LogoutView

user_urls = [
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('main', MainView.as_view(), name='main'),
    path('test', Test.as_view(), name="test"),
    # permission
    path('user/permission', PermissionMainView.as_view(), name='permission'),
    # role
    path('user/role', RoleMainView.as_view(), name='role'),
    # user
    path('user/user', UserMainView.as_view(), name="user"),
]
