from django.contrib.auth import views
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import SignUpForm


class SignUp(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('index')
    template_name = 'auth/reg.html'


class UserLogin(views.LoginView):
    template_name = 'auth/authForm.html'
    success_url = reverse_lazy('index')


class ResetPassword(views.PasswordResetView):
    template_name = 'auth/resetPassword.html'
    success_url = reverse_lazy('reset_done')


class ChangePassword(views.PasswordChangeView):
    success_url = reverse_lazy('index')
    template_name = 'auth/changePassword.html'


class ResetDone(views.PasswordResetDoneView):
    template_name = 'auth/resetDone.html'
