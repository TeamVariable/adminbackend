from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy
from django.views.generic import View, FormView
from django.core.paginator import Paginator

from .models import AdminUsers
from .forms import AdminLoginForm, AdminRegisterForm


# Create your views here.
class AdminLoginView(FormView):
    template_name: str = "visualboard/login.html"
    form_class = AdminLoginForm
    success_url = reverse_lazy("visualboard:base")
     
    def form_valid(self, form) -> HttpResponse:
        email = form.cleaned_data.get("email")
        raw_password = form.cleaned_data.get("password")
        remember_me = form.cleaned_data.get("remember_me")
        auth = authenticate(self.request, username=email, password=raw_password)
        if auth is not None:
            login(self.request, auth)
            self.request.session["remember_me"] = remember_me
        print(f"REMEMVER ME STATUS --> {self.request.session.get('remember_me')}")
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


# admin user information
def page_investigation_view(request):
    p = int(request.GET.get("p", 1))  # http://localhost/?p=1~~
    user = AdminUsers.object.all().order_by("id")
    page = Paginator(user, 10)
    page_index = page.get_page(p)
    
    return render(request, "visualboard/board.html", {"user": page_index})
    