from django.urls import path

from .views import FavoriteView, IngredientView, PurchaseView, SubscriptionView

urlpatterns = [
    path('purchases/', PurchaseView.as_view(), name='purchases'),
    path('purchases/<str:recipe_id>/',
         PurchaseView.as_view(), name='purchases'),

    path('favorites/', FavoriteView.as_view(), name='favorites'),
    path('favorites/<int:recipe_id>/',
         FavoriteView.as_view(), name='favorites'),

    path('subscriptions/', SubscriptionView.as_view(), name='subscriptions'),
    path('subscriptions/<int:author_id>/',
         SubscriptionView.as_view(), name='subscriptions'),

    path('ingredients/', IngredientView.as_view(), name='ingredients')
]
