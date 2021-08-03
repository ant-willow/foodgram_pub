from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.forms import BooleanField, CharField, Field, IntegerField
from django.shortcuts import get_object_or_404

from .models import Ingredient, Recipe, RecipeIngredient


class RecipeForm(forms.ModelForm):
    breakfast_tag = BooleanField(required=False)
    dinner_tag = BooleanField(required=False)
    supper_tag = BooleanField(required=False)

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'prep_time', 'image',
                  'breakfast_tag', 'dinner_tag', 'supper_tag']

    def __init__(self, *args, **kwargs):
        ingredients = kwargs.pop('ingredients', [])
        self.ingredients_list = []
        for ingredient in ingredients:
            self.ingredients_list.append(
                {'title': ingredient.ingredient.title,
                 'amount': ingredient.amount,
                 'units': ingredient.ingredient.unit})

        super().__init__(*args, **kwargs)


class PostRecipeForm(RecipeForm):
    error_ingredients = Field(required=False)
    error_tags = Field(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        prefix = 'nameIngredient_'
        input_names = [name for name in self.data.keys()
                       if name.startswith(prefix)]

        for name in input_names:
            number = name[len(prefix):]
            name_field = 'nameIngredient_%s' % number
            value_field = 'valueIngredient_%s' % number
            units_field = 'unitsIngredient_%s' % number

            item = {'title': self.data[name_field],
                    'amount': self.data[value_field],
                    'units': self.data[units_field]}

            self.ingredients_list.append(item)
            self.fields[name_field] = CharField()
            self.fields[value_field] = IntegerField()
            self.fields[units_field] = CharField()

    def clean(self):
        cleaned_data = super().clean()
        breakfast = cleaned_data.get('breakfast_tag')
        dinner = cleaned_data.get('dinner_tag')
        supper = cleaned_data.get('supper_tag')

        if not any((breakfast, dinner, supper)):
            self.add_error('error_tags', 'Нужно выбрать тег.')

        if not self.ingredients_list:
            self.add_error('error_ingredients', 'Нужно добавить ингредиент')

        for ingredient in self.ingredients_list:
            title = ingredient['title']
            unit = ingredient['units']
            try:
                Ingredient.objects.get(title=title, unit=unit)
            except ObjectDoesNotExist:
                self.add_error(
                    'error_ingredients', f'{title} - Такого ингредиента нет.')
                continue

    def save(self, author):
        recipe_instance = super().save(commit=False)
        recipe_instance.author = author
        recipe_instance.save()

        recipe_ingredients = (
            RecipeIngredient.objects.filter(recipe=recipe_instance))
        if recipe_ingredients.exists():
            recipe_ingredients.delete()

        for ingredient in self.ingredients_list:
            title = ingredient['title']
            amount = ingredient['amount']
            unit = ingredient['units']
            ingredient_instance = get_object_or_404(
                Ingredient, title=title, unit=unit)

            RecipeIngredient.objects.create(
                recipe=recipe_instance,
                ingredient=ingredient_instance,
                amount=amount)

        return recipe_instance
