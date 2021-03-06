from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# Create your models here.


class User(AbstractUser):
    nickname = models.CharField(max_length=32, blank=False, null=True, verbose_name="昵称")
    avatar = models.ImageField(upload_to="./media/user", verbose_name="头像")
    roles = models.ForeignKey('Role', on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="角色")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        ordering = ["id"]


class Menu(models.Model):
    """
    菜单
    """
    name = models.CharField(max_length=30, unique=True, verbose_name="菜单名")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="父菜单")
    icon = models.CharField(max_length=50, null=True, blank=True, verbose_name="图标")
    code = models.CharField(max_length=50, null=True, blank=True, verbose_name="编码")
    url = models.CharField(max_length=128, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "菜单"
        verbose_name_plural = verbose_name

    @classmethod
    def get_menu_by_request_url(cls, url):
        return dict(menu=Menu.objects.get(url))


class Role(models.Model):
    """
    角色: 用于权限绑定
    """
    name = models.CharField(max_length=30, unique=True, verbose_name="角色")
    permissions = models.ForeignKey("Menu", on_delete=models.DO_NOTHING, blank=True, verbose_name="url权限")
    desc = models.CharField(max_length=50, blank=True, null=True, verbose_name="描述")


class Department(models.Model):
    """
    组织架构
    """
    type_choice = (("unit", "单位"), ("department", "部门"))
    name = models.CharField(max_length=60, verbose_name="名称")
    type = models.CharField(max_length=30, choices=type_choice, default="department", verbose_name="类型")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, verbose_name="父部门")

    class Meta:
        verbose_name = "组织架构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

