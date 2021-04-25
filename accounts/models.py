from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AccountManager(BaseUserManager):

    def create_user(self, email, password=None):

        if not email:
            raise ValueError("使用者必須有電子郵件信箱")

        user = self.model(
            email = self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password=None):

        if not email:
            raise ValueError("管理者必須有電子郵件信箱")

        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
        )

        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self.db)
        return user


class Account(AbstractBaseUser):

    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


