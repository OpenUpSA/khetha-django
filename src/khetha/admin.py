from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as django_UserAdmin

from khetha import models


@admin.register(models.User)
class UserAdmin(django_UserAdmin):
    """
    Re-use Django's `UserAdmin`.
    """
