from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import User
from django.core.validators import RegexValidator

#'auth.User' has been swapped for 'accounts.CustomUser'


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=20,
        required=True,
        help_text=False,
        label="Tên đăng nhập",
        error_messages={
            "invalid": "Chuỗi liền bao gồm chữ,số,ký tự đặc biệt và tối đa 20 ký tự",
        },
    )
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    tel = forms.CharField(
        max_length=15,
        required=True,
        label="Số điện thoại",
        validators=[
            RegexValidator(
                regex=r"^(\+84|0){1}(9|8|7|5|3){1}[0-9]{8}$",
                message="Số điện thoại không hợp lệ",
            )
        ],
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "tel",
            "password1",
            "password2",
        )


class CompleteInformationForm(SignUpForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('email')

    class Meta:
        model = User
        fields = ("username", "tel", "password1", "password2")
