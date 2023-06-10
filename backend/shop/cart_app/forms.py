from django import forms


class UserAddressForm(forms.Form):
    delivery_address = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'})
    )
