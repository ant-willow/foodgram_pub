import json

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from recipes.models import Favorite, Ingredient, Recipe, Subscription

User = get_user_model()


class PurchaseView(View):
    def post(self, request):
        req = json.loads(request.body)
        recipe_id = req.get('id')
        if recipe_id is None:
            return JsonResponse({'success': False}, status=400)

        recipe = get_object_or_404(Recipe, id=recipe_id)
        if request.session.get('purchases') is None:
            request.session['purchases'] = dict()
        purchases = request.session['purchases']

        purchases[recipe.id] = recipe.id
        request.session.modified = True
        return JsonResponse({'success': True})

    def delete(self, request, recipe_id):
        if (request.session.get('purchases') is None
                or recipe_id not in request.session['purchases']):
            return JsonResponse({'success': False}, status=400)

        request.session['purchases'].pop(recipe_id)
        request.session.modified = True
        return JsonResponse({'success': True})


class SubscriptionView(LoginRequiredMixin, View):
    def post(self, request):
        req = json.loads(request.body)
        author_id = req.get('id')
        if author_id is None:
            return JsonResponse({'success': False}, status=400)

        author = get_object_or_404(User, id=author_id)
        _, created = Subscription.objects.get_or_create(
            user=request.user, author=author)

        if created:
            return JsonResponse({'success': True})
        return JsonResponse()

    def delete(self, request, author_id):
        subscription = get_object_or_404(
            Subscription, user=request.user, author=author_id)
        subscription.delete()
        return JsonResponse({'success': True})


class FavoriteView(LoginRequiredMixin, View):
    def post(self, request):
        req = json.loads(request.body)
        recipe_id = req.get('id')
        if recipe_id is None:
            return JsonResponse({'success': False}, status=400)

        recipe = get_object_or_404(Recipe, id=recipe_id)
        _, created = Favorite.objects.get_or_create(
            user=request.user, recipe=recipe)

        if created:
            return JsonResponse({'success': True})
        return JsonResponse()

    def delete(self, request, recipe_id):
        favorite = get_object_or_404(
            Favorite, user=request.user, recipe=recipe_id)
        favorite.delete()
        return JsonResponse({'success': True})


class IngredientView(LoginRequiredMixin, View):
    def get(self, request):
        query = self.request.GET.get('query')
        if query is None:
            return JsonResponse({'success': True})

        ingredients = Ingredient.objects.filter(title__startswith=query)
        ingredients_list = list(ingredients.values())
        return JsonResponse(ingredients_list, safe=False)
