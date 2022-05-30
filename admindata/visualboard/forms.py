from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

from typing import Dict, Tuple

from .models import AdminUsers


# RegisterForm
class AdminRegisterForm(UserCreationForm):
    error_messages: Dict[str, Tuple[str]] = {
        "password:mismatch": ("비밀번호가 맞지 않습니다 다시 입력해주세요..!")
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


# LoginForm
class AdminLoginForm(AuthenticationForm):
    error_messages: Dict[str, Tuple[str]] = {
        'invalid_login': _(
            "비밀번호나 이메일이 올바르지 않습니다 다시 입력해주세요..!"),
        'inactive': _(
            "이 계정은 비활성화 or 인증되지 않았습니다 이메일 상태를 확인해주세요..!")
    }
        
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["password"].label = "비밀번호"

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            email_check = AdminUsers.object.get(email=email)
        except AdminUsers.DoesNotExist:
            pass
        else:
            if email_check.check_password(password):
                return self.cleaned_data

