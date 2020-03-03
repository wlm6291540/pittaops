from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.deprecation import MiddlewareMixin


class LoginMiddleWare(MiddlewareMixin):

    def process_request(self, request):
        if not request.path.startswith("/login") and not request.user.is_authenticated:
            return render(request, "user/login.html")