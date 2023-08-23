from django.contrib import admin
from .models import Greeting
# Register your models here.


@admin.register(Greeting)
class GreetingAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "user", "created_at")
    search_fields = ("text", "user__username")
    readonly_fields = ("created_at", "last_modified_at")

    # fieldsets = (
    #     (None, {"fields": ("text", "user")}),
    #     ("Date information", {"fields": ("created_at", "last_modified_at"),},),
    # )