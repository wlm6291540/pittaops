import json

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic import TemplateView, View, RedirectView

from user.models import Department
from user.forms import DepartmentForm


# Create your views here.

class MainView(TemplateView):
    template_name = 'index.html'


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


class DepartmentMainView(TemplateView):
    template_name = 'user/department/main.html'


class RoleMainView(TemplateView):
    template_name = 'user/role/main.html'


class PermissionMainView(TemplateView):
    template_name = 'user/permission/main.html'


# department view
class DepartmentCreateView(View):

    def get(self, request):
        ret = dict(result=True, departments=Department.objects.all())
        return render(request, 'user/department/add.html', ret)

    def post(self, request):
        ret = dict(result=True)
        dept = Department()
        dept_form = DepartmentForm(request.POST, instance=dept)
        if dept_form.is_valid():
            dept.save()
            ret['result'] = True
        return HttpResponse(json.dumps(ret), content_type="application/json")


class DepartmentListView(View):
    def get(self, request):
        fields = ['id', 'name', 'type', 'parent__name']
        data = list(Department.objects.values(*fields).order_by('id'))
        total = len(data)
        ret = dict(total=total, rows=data)
        return HttpResponse(json.dumps(ret), content_type='application/json')


class DepartmentTreeListView(View):
    def get(self, request):
        ret = []
        fields = ['id', 'name', 'type', 'parent', 'parent__name']
        top = list(Department.objects.values(*fields).filter(parent=None))
        for item in top:
            temp = {**item, "sub": list(Department.objects.values(*fields).filter(parent=item["id"]))}
            ret.append(temp)

        return HttpResponse(json.dumps(dict(data=ret)), content_type="application/json")

