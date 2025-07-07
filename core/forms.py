from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('technician', 'Technician'),
    )
    photo = forms.ImageField(required=False)
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)
    category = forms.ChoiceField(
        choices=CustomUser.CATEGORY_CHOICES,
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role', 'category', 'photo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'placeholder': 'Only for technicians'})
