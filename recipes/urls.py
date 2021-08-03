from django.urls import path

from .views import (AuthorView, DeleteRecipeView, EditRecipeView, FavoriteView,
                    Index, NewRecipeView, RecipeView, ShoppingListDownloadView,
                    ShoppingListView, SubscriptionView)

urlpatterns = [
    path('', Index.as_view(), name='index'),

    path('subscriptions/', SubscriptionView.as_view(), name='subscriptions'),
    path('favorites/', FavoriteView.as_view(), name='favorites'),
    path('shopping-list/', ShoppingListView.as_view(), name='shopping_list'),
    path('shopping-list/download/',
         ShoppingListDownloadView.as_view(), name='shopping_list_download'),

    path('recipe/new/', NewRecipeView.as_view(), name='new_recipe'),
    path('recipe/<int:recipe_id>/', RecipeView.as_view(), name='view_recipe'),
    path('recipe/<int:recipe_id>/edit/',
         EditRecipeView.as_view(), name='edit_recipe'),
    path('recipe/<int:recipe_id>/delete/',
         DeleteRecipeView.as_view(), name='delete_recipe'),

    path('<str:username>/', AuthorView.as_view(), name='view_author'),
]
