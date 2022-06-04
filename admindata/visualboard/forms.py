from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


from .models import AdminUsers
from typing import Dict, Tuple



# RegisterForm
class AdminRegisterForm(UserCreationForm):
    error_messages: Dict[str, str] = {
        "password_mismatch": "비밀번호가 맞지 않습니다 다시 입력해주세요..!"
    }
    full_name = forms.CharField(
        max_length=20, label="이름",
        widget=forms.TextInput(attrs={"class": "name", "placeholder": "성함"})
    )

    class Meta:
        model = AdminUsers
        fields = ("full_name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for num in range(1, 3):
            self.fields[f'password{num}'].label = f"패스워드{num}"
            self.fields[f"password{num}"].widget.attrs.update({
                "class": f"password{num}-control",
                "placeholder": f"password{num}-checking"
            })

    def clean_password2(self) -> str:
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2 :
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code = "password_mismatch"
            )
        return super().clean_password2()


# LoginForm
class AdminLoginForm(forms.Form):
    error_messages: Dict[str, str] = {
        'invalid_login': _(
            "없는 이메일 이거나 비밀번호나 이메일이 올바르지 않습니다 다시 입력해주세요..!"),
        'inactive': _(
            "이 계정은 비활성화 or 인증되지 않았습니다 이메일 상태를 확인해주세요..!")
    }
    
    email = forms.CharField(
        max_length=50, required=True, label="이메일",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter Email Addreadd"})
    )
    password = forms.CharField(
        max_length=50, required=False, label="패스워드",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"})
    )
    remember_me = forms.BooleanField(
        required=False, disabled=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-control-input", "id": "customCheck"}),
    )
    
    
    def get_invalid_login_error(self) -> ValidationError:
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
        )
    
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            email_check = AdminUsers.object.get(email=email)
            print(f"form -> {email}, form -> {password}")
            if email_check.check_password(password):
                return self.cleaned_data
            else:
                raise self.get_invalid_login_error()
        except AdminUsers.DoesNotExist:
            raise self.get_invalid_login_error()
            

