import pytest

from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Diet, Recipe


class RecipeModelTests(TestCase):
    def test_create_recipe(self):
        recipe = Recipe.objects.create(
            name="Yakisoba",
            description="Japanese stir-fried noodles.",
            instructions="Stir-fry the ingredients and noodles.",
            diet=Diet.VEG,
            cuisine=["japanese"],
            difficulty=2,
        )

        self.assertEqual(recipe.name, "Yakisoba")
        self.assertEqual(recipe.diet, Diet.VEG)
        self.assertEqual(recipe.cuisine, ["japanese"])
        self.assertEqual(recipe.difficulty, 2)

    def test_diet_choices(self):
        self.assertEqual(
            dict(Diet.choices),
            {
                "veg": "Vegetarian",
                "non_veg": "Non-vegetarian",
                "eggetarian": "Eggetarian",
                "pescatarian": "Pescatarian",
                "sattvik": "Sattvik",
            },
        )

    def test_difficulty_must_be_between_one_and_five(self):
        recipe = Recipe(
            name="Test Recipe",
            instructions="Test instructions",
            diet=Diet.VEG,
            difficulty=0,
        )

        with self.assertRaises(ValidationError):
            recipe.full_clean()

        recipe.difficulty = 6

        with self.assertRaises(ValidationError):
            recipe.full_clean()

    def test_difficulty_accepts_boundary_values(self):
        for difficulty in (1, 5):
            recipe = Recipe(
                name="Test Recipe",
                instructions="Test instructions",
                diet=Diet.VEG,
                difficulty=difficulty,
            )

            recipe.full_clean()

    def test_cuisine_defaults_to_empty_list(self):
        recipe = Recipe.objects.create(
            name="Test Recipe",
            instructions="Test instructions",
            diet=Diet.VEG,
            difficulty=1,
        )

        self.assertEqual(recipe.cuisine, [])

    def test_timestamps_are_set(self):
        recipe = Recipe.objects.create(
            name="Test Recipe",
            instructions="Test instructions",
            diet=Diet.VEG,
            difficulty=1,
        )

        self.assertIsNotNone(recipe.created_at)
        self.assertIsNotNone(recipe.updated_at)

    def test_cuisine_labels_are_human_readable(self):
        recipe = Recipe(
            name="Korean-Italian Fusion",
            instructions="...",
            diet=Diet.VEG,
            cuisine=["korean", "italian"],
            difficulty=3,
        )

        assert recipe.cuisine_labels == ["Korean", "Italian"]


@pytest.mark.django_db
def test_recipe_list_returns_200(client):
    response = client.get("/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_recipe_list_can_search_by_name(client):
    Recipe.objects.create(
        name="Oyakodon",
        description="Japanese rice bowl",
        instructions="Cook...",
        diet=Diet.EGGETARIAN,
        cuisine=["japanese"],
        difficulty=2,
    )

    Recipe.objects.create(
        name="Palak Paneer",
        description="Indian spinach and paneer dish",
        instructions="Cook...",
        diet=Diet.NON_VEG,
        cuisine=["indian"],
        difficulty=2,
    )

    response = client.get("/", {"q": "oyako"})

    assert response.status_code == 200
    assert "Oyakodon" in response.content.decode()
    assert "Palak Paneer" not in response.content.decode()
