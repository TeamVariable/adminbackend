from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views.generic import View, FormView


from .models import AdminUsers
from .forms import AdminLoginForm, AdminRegisterForm


# Create your views here.
class AdminLoginView(FormView):
    template_name: str = "visualboard/login.html"
    form_class = AdminLoginForm
    success_url = "/admindash/base/"

    def form_valid(self, form) -> HttpResponse:
        email = form.cleaned_data.get("email")
        raw_password = form.cleaned_data.get("password")
        auth_user = authenticate(self.request, username=email, password=raw_password)
        print(email, raw_password, auth_user)
        if auth_user is not None:
            login(self.request, auth_user)
        return super().form_valid(form)


class AdminRegisterView(FormView):
    template_name: str = "visualboard/register.html"
    form_class = AdminRegisterForm
    success_url = "/admindash/login/"
    
    def form_valid(self, form) -> HttpResponse:
        form.save()
        return super().form_valid(form)
    

def logout_view(request):
    logout(request)
    return redirect("index")
