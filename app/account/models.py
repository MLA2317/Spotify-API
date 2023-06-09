from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db.models.signals import pre_save
from django.utils.safestring import mark_safe


class AccountManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if username is None:
            raise TypeError('User should have a username')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username=username, password=password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    username = models.CharField(max_length=60, unique=True, verbose_name='Username', db_index=True)
    avatar = models.ImageField(upload_to='avatar/')
    is_superuser = models.BooleanField(default=False, verbose_name='Super user')
    is_staff = models.BooleanField(default=False, verbose_name='Staff')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Created Date')

    object = AccountManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def image_tag(self):
        if self.avatar:
            return mark_safe(f"<a href='{self.avatar.url}'><img src='{self.avatar.url}' style='height:43px;'/></a>")
        else:
            return 'Image not found'



