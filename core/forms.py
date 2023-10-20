from django import forms
from .models import Contact
from django.core.validators import RegexValidator
from django import forms


class ContactForm(forms.ModelForm):
    name = forms.CharField(
        max_length=20,
        required=True,
        help_text=False,
        label="Họ và tên"
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
    content = forms.CharField(
        required=True,
        help_text=False,
        label="Nội dung",
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}),
    )

    class Meta:
        model = Contact
        fields = [
            "name",
            "email",
            "tel",
            "content"
        ]


# tỉnh/tpho-province/city
# quận/huyện-District
# phường/xã-wards
# địa chỉ cụ thể -specific-address