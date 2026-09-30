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
