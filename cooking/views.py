import logging

from django.db import models
from django.shortcuts import get_object_or_404, render

from .models import Recipe

logger = logging.getLogger(__name__)


def recipe_list(request):
    all_recipes = Recipe.objects.all()
    recipes = all_recipes.order_by("-created_at")

    query = request.GET.get("q", "").strip()
    diet = request.GET.get("diet", "").strip()
    cuisine = request.GET.get("cuisine", "").strip()

    if query:
        recipes = recipes.filter(
            models.Q(name__icontains=query) | models.Q(description__icontains=query)
        )

    if diet:
        recipes = recipes.filter(diet=diet)

    if cuisine:
        recipes = recipes.filter(cuisine__contains=[cuisine])

    cuisines = sorted({cuisine for recipe in all_recipes for cuisine in recipe.cuisine})

    context = {
        "recipes": recipes,
        "query": query,
        "selected_diet": diet,
        "selected_cuisine": cuisine,
        "diet_choices": Recipe._meta.get_field("diet").choices,
        "cuisine_options": [
            (
                value,
                value.replace("_", " ").title(),
            )
            for value in cuisines
        ],
    }

    logger.info(
        "Recipe list view accessed with query='%s', diet='%s', cuisine='%s'",
        query,
        diet,
        cuisine,
    )

    return render(
        request,
        "cooking/recipe_list.html",
        context,
    )


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    logger.info("Recipe detail view accessed for recipe with pk='%s'", pk)

    return render(
        request,
        "cooking/recipe_detail.html",
        {"recipe": recipe},
    )
