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

    def form_invalid(self, form) -> HttpResponse:
        return super().form_invalid(form)
    
    def form_valid(self, form) -> HttpResponse:
        email = form.cleaned_data.get("email")
        raw_password = form.cleaned_data.get("password")
        auth_user = authenticate(self.request, email=email, password=raw_password)
        print(email, raw_password, auth_user)
        if auth_user is not None:
            login(self.request, auth_user)
        return super().form_valid(form)


class AdminRegisterView(View):
    form_class = AdminRegisterForm
    template_name: str = "visualboard/register.html"

    def get(self, request):
        forms = self.form_class()
        return render(request, self.template_name, {"form": forms})

    def post(self, request):
        forms = self.form_class(request.POST)
        msg = "올바르지 않는 형식입니다 다시입력해주세요..!"
        if forms.is_valid():
            forms.save()
            return HttpResponseRedirect("/admindash/login/")
        return render(request, self.template_name, {"form": forms, "msg": msg})


def logout_view(request):
    logout(request)
    return redirect("index")
