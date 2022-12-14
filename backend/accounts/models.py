from django.db import models
from django.core.validators import validate_email
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class UserAccountManager(BaseUserManager):
    def create_user(self, email: str, password: str):
        if not email:
            raise ValueError("Users must have an email address.")

        if not password:
            raise ValueError("Users must have an password.")

        validate_email(email)

        if len(password) < 6:
            raise ValueError("Password should be atleast 6 character long.")

        email = self.normalize_email(email)
        user = self.model(email=email)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email: str, password: str):
        user = self.create_user(email, password)

        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model for User Account
    """

    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"

    def get_full_name(self):
        return str(self.email)

    def get_short_name(self):
        return str(self.email)

    def __str__(self):
        return str(self.email)
