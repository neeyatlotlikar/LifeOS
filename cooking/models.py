from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Diet(models.TextChoices):
    VEG = "veg", "Vegetarian"
    NON_VEG = "non_veg", "Non-vegetarian"
    EGGETARIAN = "eggetarian", "Eggetarian"
    PESCATARIAN = "pescatarian", "Pescatarian"
    SATTVIK = "sattvik", "Sattvik"


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    instructions = models.TextField()

    diet = models.CharField(
        max_length=20,
        choices=Diet,
    )

    cuisine = models.JSONField(default=list, blank=True)

    difficulty = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def cuisine_labels(self):
        return [value.replace("_", " ").title() for value in self.cuisine]
