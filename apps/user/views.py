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
        status = True
        message = "添加成功"
        data = request.POST
        pid = data.get('parent', None)
        dtype = data.get('type', None)
        name = data.get('name', None)
        try:
            if pid is None and dtype == 'unit':
                if len(Department.objects.filter(name=name, type=dtype).all()) < 1:
                    dept = Department(name=name, type=dtype)
                    dept.save()
                else:
                    status = False
                    message = "存在同名的单位"
            elif (pid is None or len(pid) < 1) and dtype != 'unit':
                status = False
                message = "不能创建没有上级单位的部门"
            elif pid and dtype == 'unit':
                status = False
                message = "不能创建有上级部门的单位"
            else:
                pdept = None
                if len(pid) > 0:
                    pdept = Department.objects.get(id=pid)
                if len(Department.objects.filter(name=name, type=dtype, parent=pdept).all()) < 1:
                    dept = Department(name=name, type=dtype, parent=pdept)
                    dept.save()
                else:
                    status = False
                    message = "存在同名的部门"
        except ValueError as e:
            status = False
            message = "系统内部错误"
            print(e)
        ret = dict(result=status, msg=message)
        return HttpResponse(json.dumps(ret), content_type="application/json")


class DepartmentListView(View):
    def get(self, request):
        fields = ['id', 'name', 'type', 'parent', 'parent__name']
        data = list(Department.objects.values(*fields).order_by('id'))
        total = len(data)
        ret = dict(total=total, rows=data)
        return HttpResponse(json.dumps(ret), content_type='application/json')


class DepartmentDeleteView(View):
    def post(self, request):
        status = True
        message = "删除成功"
        data = request.POST.get('id', None)
        if data:
            data = json.loads(data)
            dept = Department.objects.get(id=data)
            dept.delete()
        else:
            status = False
            message = "删除失败"
        ret = dict(result=status, msg=message)
        return HttpResponse(json.dumps(ret), content_type='application/json')


# department view
class DepartmentUpdateView(View):
    def post(self, request):
        status = True
        message = "添加成功"
        data = request.POST
        id = data.get('id', None)
        pid = data.get('parent', None)
        dtype = data.get('type', None)
        name = data.get('name', None)
        try:
            if pid is None and dtype == 'unit':
                if len(Department.objects.filter(name=name, type=dtype).all()) < 1:
                    dept = Department.objects.get(id=id)
                    dept.type = dtype
                    dept.name = name
                    dept.save()
                else:
                    status = False
                    message = "存在同名的单位"
            elif (pid is None or len(pid) < 1) and dtype != 'unit':
                status = False
                message = "不能创建没有上级单位的部门"
            elif pid and dtype == 'unit':
                status = False
                message = "不能创建有上级部门的单位"
            else:
                pdept = None
                if len(pid) > 0:
                    pdept = Department.objects.get(id=pid)
                if len(Department.objects.filter(name=name, type=dtype, parent=pdept).all()) < 1:
                    dept = Department.objects.get(id=id)
                    dept.parent = pdept
                    dept.type = dtype
                    dept.name = name
                    dept.save()
                else:
                    status = False
                    message = "存在同名的部门"
        except ValueError as e:
            status = False
            message = "系统内部错误"
            print(e)
        ret = dict(result=status, msg=message)
        return HttpResponse(json.dumps(ret), content_type="application/json")