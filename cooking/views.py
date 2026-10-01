from django.shortcuts import get_object_or_404, render

from .models import Recipe


def recipe_list(request):
    recipes = Recipe.objects.all().order_by("-created_at")

    return render(
        request,
        "cooking/recipe_list.html",
        {"recipes": recipes},
    )


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    return render(
        request,
        "cooking/recipe_detail.html",
        {"recipe": recipe},
    )
