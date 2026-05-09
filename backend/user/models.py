from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, userName, password=None, **extra_fields):
        """创建普通用户"""
        if not userName:
            raise ValueError('用户名必须提供')
        
        # 处理 email
        email = extra_fields.pop('email', None)
        if email:
            email = self.normalize_email(email)
        
        user = self.model(
            userName=userName,
            email=email,
            register=timezone.now(),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, userName, password=None, **extra_fields):
        """创建超级用户"""
        extra_fields.setdefault('status', 'active')
        extra_fields.setdefault('userType', 'head')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(userName, password, **extra_fields)


DEFAULT_AVATAR = "https://niu.codejourney.cn/static/userAvatar/default.png"

class User(AbstractBaseUser, PermissionsMixin):
    """继承 Django 认证基类"""
    STATUS_CHOICES = [
        ("active", "启用"),
        ("inactive", "禁用"),
    ]
    SEX_CHOICES = [
        ("boy", "男"),
        ("girl", "女"),
        ("notall", "保密")
    ]
    USERTYPE_CHOICES = [
        ("head", "站长"),
        ("general", "普通用户")
    ]

    # 主键
    userId = models.AutoField(primary_key=True, verbose_name="ID")
    
    # 登录相关字段
    userName = models.CharField(max_length=128, null=False, unique=True, verbose_name="用户名")
    phone = models.CharField(max_length=11, null=True, unique=True, blank=True, verbose_name="电话号码")
    email = models.EmailField(max_length=128, null=True, unique=True, blank=True, verbose_name="邮箱")
    password = models.CharField(max_length=256, null=False, verbose_name="密码")
    
    # 用户信息
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active", verbose_name="状态")
    userSex = models.CharField(max_length=10, choices=SEX_CHOICES, default="notall", verbose_name="性别")
    avatar = models.CharField(max_length=256, null=True, blank=True, default=DEFAULT_AVATAR,verbose_name="头像")
    introduce = models.CharField(max_length=256, default="此人很懒,未留下任何简介~", verbose_name="简介")
    userType = models.CharField(max_length=10, choices=USERTYPE_CHOICES, default="general", verbose_name="用户类型")
    register = models.DateTimeField(default=timezone.now, verbose_name="注册时间")
    
    # Django 认证系统需要的字段
    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    is_staff = models.BooleanField(default=False, verbose_name="是否员工")
    is_superuser = models.BooleanField(default=False, verbose_name="是否超级用户")
    last_login = models.DateTimeField(null=True, blank=True, verbose_name="最后登录")
    
    # 使用自定义管理器
    objects = UserManager()
    
    # 指定认证字段
    USERNAME_FIELD = 'userName'  # 用哪个字段登录
    
    # 创建超级用户时需要哪些字段
    REQUIRED_FIELDS = ['email']
    
    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-register']
    
    def __str__(self):
        return self.userName
    
    def has_perm(self, perm, obj=None):
        """检查用户权限"""
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        """检查用户是否有应用权限"""
        return self.is_superuser
    
    @property
    def is_admin(self):
        """是否是管理员"""
        return self.userType == 'head'
    
    def get_full_name(self):
        """获取全名"""
        return self.userName
    
    def get_short_name(self):
        """获取简称"""
        return self.userName
