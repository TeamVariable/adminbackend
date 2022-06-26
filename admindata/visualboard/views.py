from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout, authenticate


from .models import AdminUsers
from .forms import AdminLoginForm, AdminRegisterForm


# Create your views here.

# dash index LoginRequireMixin 상속
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name: str = "visualboard/base.html"
    redirect_field_name: str = "/admindash/login/"
    

# View 로 refactoring 고민 
class AdminLoginView(FormView):
    template_name: str = "visualboard/login.html"
    form_class = AdminLoginForm
    success_url = reverse_lazy("visualboard:base")
        
    def form_valid(self, form) -> HttpResponse:
        form_data = form.clean()
        if form_data is not None:
            auth = authenticate(self.request, username=form_data["email"], password=form_data["password"])
            login(self.request, auth)
            self.request.session["remember_me"] = form_data["remember_me"]
            
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
    return redirect("visualboard:login")


# admin user information
def page_investigation_view(request):
    p = int(request.GET.get("p", 1))  # http://localhost/?p=1~~
    user = AdminUsers.object.all().order_by("id")  # spring boot data format architecture one of data injection 
    page = Paginator(user, 10)
    page_index = page.get_page(p)
    
    return render(request, "visualboard/board.html", {"user": page_index})
    