from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views.generic import View, FormView


from .models import AdminUsers
from .forms import AdminLoginForm, AdminRegisterForm


# Create your views here.
class AdminLoginView(View):
    template_name: str = "visualboard/login.html"
    form_class = AdminLoginForm
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})
    
    def post(self, request):
        form = self.form_class(data=self.request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            auth = authenticate(self.request, username=email, password=raw_password)
            if auth is not None:
                login(self.request, auth)
                return HttpResponseRedirect("/admindash/base/")
        return render(request, self.template_name, {"form": form})
            
        
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
