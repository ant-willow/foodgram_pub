from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import ChangePassword, ResetDone, ResetPassword, SignUp, UserLogin

urlpatterns = [
    path('signup/', SignUp.as_view(), name='sign_up'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', UserLogin.as_view(), name='login'),
    path('change-password/', ChangePassword.as_view(), name='change_password'),
    path('reset-password/', ResetPassword.as_view(), name='reset_password'),
    path('reset-done/', ResetDone.as_view(), name='reset_done'),
]
