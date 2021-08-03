import io

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic.edit import FormView

from .forms import PostRecipeForm, RecipeForm
from .mixins import AnnotateFavoriteMixin, PaginatorMixin, TagFilterMixin
from .models import Recipe, RecipeIngredient, User
from .pdf import PDFMaker


class Index(View, AnnotateFavoriteMixin, PaginatorMixin, TagFilterMixin):
    def get(self, request):
        recipes_list = Recipe.objects.select_related('author')
        recipes_list = self.tag_filter(recipes_list)
        recipes_list = self.annotate_favorited(recipes_list)
        paginator, page = self.set_paginator(recipes_list)
        context = {'page': page, 'paginator': paginator}
        return render(request, 'index.html', context)


class SubscriptionView(LoginRequiredMixin, View, PaginatorMixin):
    def get(self, request):
        subscriptions = request.user.subscriptions
        authors_list = User.objects.filter(
            pk__in=subscriptions.values('author'))
        authors_list = authors_list.annotate(num_recipes=Count('recipes') - 3)
        paginator, page = self.set_paginator(authors_list)
        context = {'page': page, 'paginator': paginator}
        return render(request, 'myFollow.html', context)


class FavoriteView(LoginRequiredMixin, View,
                   AnnotateFavoriteMixin, PaginatorMixin, TagFilterMixin):
    def get(self, request):
        favorites = request.user.favorites.select_related('recipe')
        recipes_list = (Recipe.objects
                        .filter(pk__in=favorites.values('recipe'))
                        .select_related('author'))
        recipes_list = self.tag_filter(recipes_list)
        paginator, page = self.set_paginator(recipes_list)
        context = {'page': page, 'paginator': paginator}
        return render(request, 'favorite.html', context)


class AuthorView(View, AnnotateFavoriteMixin, PaginatorMixin, TagFilterMixin):
    def get(self, request, username):
        author = get_object_or_404(User, username=username)
        recipes_list = self.annotate_favorited(author.recipes.all())
        recipes_list = self.tag_filter(recipes_list)
        paginator, page = self.set_paginator(recipes_list)

        context = {'author': author, 'page': page, 'paginator': paginator}
        return render(request, 'authorRecipe.html', context)


class RecipeView(View):
    def get(self, request, recipe_id):
        recipe = get_object_or_404(
            Recipe.objects.select_related('author'), id=recipe_id)
        author = recipe.author
        ingredients_list = (
            RecipeIngredient.objects.filter(recipe=recipe)
            .select_related('ingredient'))

        context = {'author': author, 'recipe': recipe,
                   'ingredients': ingredients_list}
        return render(request, 'singlePage.html', context)


class NewRecipeView(LoginRequiredMixin, FormView):
    def get(self, request):
        form = RecipeForm()
        return render(request, 'formRecipe.html', {'form': form})

    def post(self, request):
        form = PostRecipeForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save(request.user)
            return redirect(reverse('index'))
        return render(request, 'formRecipe.html', {'form': form})


class EditRecipeView(LoginRequiredMixin, FormView):
    def get(self, request, recipe_id):
        recipe = get_object_or_404(
            Recipe.objects.select_related('author'), id=recipe_id)
        if request.user != recipe.author:
            return redirect(reverse('view_recipe', args=(recipe_id,)))

        ingredients = RecipeIngredient.objects.filter(recipe=recipe)

        form = RecipeForm(
            ingredients=ingredients,
            instance=recipe)
        context = {'form': form, 'recipe_id': recipe_id}
        return render(request, 'formRecipe.html', context)

    def post(self, request, recipe_id):
        recipe = get_object_or_404(
            Recipe.objects.select_related('author'), id=recipe_id)
        if request.user != recipe.author:
            return redirect(reverse('view_recipe', args=(recipe_id,)))

        form = PostRecipeForm(
            request.POST,
            files=request.FILES,
            instance=recipe)
        context = {'form': form, 'recipe_id': recipe_id}

        if form.is_valid():
            form.save(request.user)
            return redirect(reverse('view_recipe', args=(recipe_id,)))
        return render(request, 'formRecipe.html', context)


class DeleteRecipeView(LoginRequiredMixin, View):
    def get(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if request.user != recipe.author:
            return redirect(reverse('view_recipe', args=(recipe_id,)))
        recipe.delete()
        return redirect(reverse('index'))


class ShoppingListView(View):
    def get(self, request):
        if request.session.get('purchases') is not None:
            shopping_list = Recipe.objects.filter(
                pk__in=request.session['purchases'].keys())
            context = {'shopping_list': shopping_list}
        else:
            context = {}
        return render(request, 'shopList.html', context)


class ShoppingListDownloadView(View):
    def get(self, request):
        if request.session.get('purchases') is None:
            return redirect(reverse('shopping_list'))

        recipes = request.session['purchases'].keys()
        recipe_ingredients = (
            RecipeIngredient.objects.filter(recipe__in=recipes))

        shop_dict = {}
        for ing in recipe_ingredients:
            title = ing.ingredient.title
            amount = ing.amount
            units = ing.ingredient.unit
            if title in shop_dict:
                shop_dict[title][0] += amount
            else:
                shop_dict[title] = [amount, units]

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = (
            'attachment; filename="Shopping List.pdf"')

        buffer = io.BytesIO()
        maker = PDFMaker(buffer, 'A4')
        pdf = maker.create_pdf(shop_dict)
        response.write(pdf)
        return response
