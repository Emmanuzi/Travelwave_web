from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    """Form for updating user profile information."""

    class Meta:
        model = Profile
        fields = ["phone_number", "location", "bio"]
        widgets = {
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


