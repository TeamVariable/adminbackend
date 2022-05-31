from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy
from django.views.generic import View, FormView


from .models import AdminUsers
from .forms import AdminLoginForm, AdminRegisterForm


# Create your views here.
class AdminLoginView(FormView):
    template_name: str = "visualboard/login.html"
    form_class = AdminLoginForm
    success_url = reverse_lazy("visualboard:base")
     
    def form_valid(self, form) -> HttpResponse:
        email = form.cleaned_data.get("username")
        raw_password = form.cleaned_data.get("password")
        auth = authenticate(self.request, username=email, password=raw_password)
        if auth is not None:
            login(self.request, auth)
        return super().form_valid(form)
    

class AdminRegisterView(FormView):
    template_name: str = "visualboard/register.html"
    form_class = AdminRegisterForm
    success_url = reverse_lazy("visualboard:login")
    
    def form_valid(self, form) -> HttpResponse:
        form.save()
        return super().form_valid(form)
    

def logout_view(request):
    logout(request)
    return redirect("index")
