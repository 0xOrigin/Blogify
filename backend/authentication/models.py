import os
import uuid
from enum import Enum
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from core.models import BaseManager, BaseAuditModel


class UserManager(BaseUserManager, BaseManager):

    def create_user(self, email, username, password=None, created_at=timezone.now()):
        if not email:
            raise ValueError(_('User must have an email address'))
        if not username:
            raise ValueError(_('User must have a username'))

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            created_at=created_at,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, BaseAuditModel, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']
    objects = UserManager()

    class Meta:
        managed = True
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['username']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self) -> str:
        return self.email