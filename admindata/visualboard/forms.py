from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import AdminUsers
from typing import Dict


# RegisterForm
class AdminRegisterForm(UserCreationForm):
    error_messages: Dict[str, str] = {
        "password_mismatch": "비밀번호가 맞지 않습니다 다시 입력해주세요..!"
    }
    full_name: forms = forms.CharField(
        max_length=20, label="name",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "이름"})
    )

    class Meta:
        model = AdminUsers
        fields = ("full_name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "이메일"
        })
        for num in range(1, 3):
            self.fields[f"password{num}"].widget.attrs.update({
                "class": "form-control",
                "placeholder": f"패스워드 {num}번-확인"
            })

    def clean_password2(self) -> str:
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch"
            )
        return super().clean_password2()


# LoginForm
class AdminLoginForm(forms.Form):
    error_messages: Dict[str, str] = {
        'invalid_login': _("비밀번호나 이메일이 올바르지 않습니다"),
        'inactive': _(
            "이 계정은 비활성화 or 인증되지 않았습니다 이메일 상태를 확인해주세요..!")
    }

    email: forms = forms.CharField(
        max_length=50, required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "이메일"})
    )
    password: forms = forms.CharField(
        max_length=50, required=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "패스워드"})
    )
    remember_me: forms = forms.BooleanField(
        required=False, disabled=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-control-input", "id": "customCheck"}),
    )

    def get_invalid_login_error(self) -> ValidationError:
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
        )

    def clean(self):
        email: str = self.cleaned_data.get("email")
        password: str = self.cleaned_data.get("password")
        remember_me: bool = self.cleaned_data.get("remember_me")
        try:
            email_check = AdminUsers.object.get(email=email)
            print(f"form -> {email_check}, password -> {password}, remember_me -> {remember_me}")
            if email_check.check_password(password):
                return self.cleaned_data
            else:
                raise self.get_invalid_login_error()
        except AdminUsers.DoesNotExist:
            raise self.get_invalid_login_error()
