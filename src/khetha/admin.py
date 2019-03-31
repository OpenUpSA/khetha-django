from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.auth.admin import UserAdmin as django_UserAdmin

from khetha import models

# Tweaked InlineModelAdmin defaults:


class _InlineModelAdmin(InlineModelAdmin):
    extra = 0
    show_change_link = True


class _TabularInline(admin.TabularInline, _InlineModelAdmin):
    pass


@admin.register(models.User)
class UserAdmin(django_UserAdmin):
    """
    Re-use Django's `UserAdmin`.
    """


class QuestionInline(_TabularInline):
    model = models.Question
    exclude = ["description"]
    raw_id_fields = ["task"]


class AnswerOptionInline(_TabularInline):
    model = models.AnswerOption
    raw_id_fields = ["question"]


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["slug", "title", "description", "points", "is_published"]
    search_fields = ["slug", "title", "description"]
    list_editable = ["is_published"]
    list_filter = ["is_published"]

    inlines = [QuestionInline]


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["text", "task"]
    raw_id_fields = ["task"]

    inlines = [AnswerOptionInline]


@admin.register(models.AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ["text", "question"]
    raw_id_fields = ["question"]
