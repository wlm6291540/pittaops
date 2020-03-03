from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from user.views import LoginView, UserMainView, PermissionMainView, RoleMainView, MainView
from user.views import LogoutView, DepartmentMainView
from user.views import DepartmentCreateView, DepartmentListView, DepartmentTreeListView

user_urls = [
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('main', MainView.as_view(), name='main'),

    # permission
    path('user/permission', PermissionMainView.as_view(), name='permission'),
    # role
    path('user/role', RoleMainView.as_view(), name='role'),
    # user
    path('user/user', UserMainView.as_view(), name="user"),
]

# department
dept_urls = [
    path('user/department', DepartmentMainView.as_view(), name='department'),
    path('user/department/create', DepartmentCreateView.as_view(), name='department create'),
    path('user/department/list', DepartmentListView.as_view(), name='department list'),
    path('user/department/tree', DepartmentTreeListView.as_view(), name='department tree list'),
]

user_urls += dept_urls
