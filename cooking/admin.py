from django.contrib import admin

from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "diet",
        "difficulty",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "diet",
        "difficulty",
    )
    search_fields = (
        "name",
        "description",
        "instructions",
    )
