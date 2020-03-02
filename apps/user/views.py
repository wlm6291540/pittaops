from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic import TemplateView, View, RedirectView


# Create your views here.

class MainView(TemplateView):
    template_name = 'index.html'

18152069690

class LoginView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'user/login.html', )
        else:
            return HttpResponseRedirect("/")

    def post(self, request, *args, **kwargs):
        parameter = request.POST
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('main')
        else:
            return HttpResponseRedirect("/login")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("login"))


class UserMainView(TemplateView):
    template_name = 'user/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Test(TemplateView):
    template_name = 'user/test.html'


class RoleMainView(TemplateView):
    template_name = 'user/role/main.html'


class PermissionMainView(TemplateView):
    template_name = 'user/permission/main.html'

