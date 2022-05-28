from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views.generic import View, FormView
from django.urls import reverse_lazy

from .models import AdminUsers
from .forms import AdminLoginForm, AdminRegisterForm


# Create your views here.
class AdminLoginView(FormView):
    template_name: str = "visualboard/login.html"
    form_class = AdminLoginForm
    success_url = reverse_lazy("visualboard:base")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pass

    def form_valid(self, form):
        pass


class AdminRegisterView(View):
    form_class = AdminRegisterForm
    template_name: str = "visualboard/register.html"

    def get(self, request):
        pass

    def post(self, request):
        pass


def logout_view(request):
    logout(request)
    return redirect("index")
