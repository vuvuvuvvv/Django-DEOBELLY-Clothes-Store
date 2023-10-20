from django import forms
from .models import Order
from django.core.validators import RegexValidator
from django import forms

class OrderForm(forms.ModelForm):
    consignee_name = forms.CharField(
        max_length=20,
        required=True,
        help_text=False,
        label="Họ và tên người nhận"
    )
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
    specific_address = forms.CharField(
        max_length=150,
        required=True,
        help_text=False,
        label="Địa chỉ cụ thể"
    )
    notes = forms.CharField(
        required=False,
        help_text=False,
        label="Ghi chú cho người bán",
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}),
    )

    class Meta:
        model = Order
        fields = [
            "consignee_name",
            "tel",
            "specific_address",
            "notes"
        ]