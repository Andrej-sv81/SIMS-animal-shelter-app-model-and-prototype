from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Adopter, Animal, BankStatement, Organization


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Korisničko ime"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Lozinka"}))


class VolunteerRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    organization = forms.ModelChoiceField(queryset=Organization.objects.filter(is_active=True), widget=forms.Select(attrs={"class": "form-select"}))

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise ValidationError("Korisničko ime već postoji.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Lozinke se ne poklapaju.")
        return cleaned_data


class OrganizationCreateForm(forms.ModelForm):
    admin_username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    admin_email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "form-control"}))
    admin_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    admin_password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = Organization
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def clean_admin_username(self):
        username = self.cleaned_data.get("admin_username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Korisničko ime već postoji.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("admin_password")
        password_confirm = cleaned_data.get("admin_password_confirm")
        if password and password_confirm and password != password_confirm:
            raise ValidationError("Lozinke se ne poklapaju.")
        return cleaned_data


class OrganizationEditForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ["name", "status", "image"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class AdopterForm(forms.ModelForm):
    class Meta:
        model = Adopter
        fields = ["first_name", "last_name", "phone", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


class AdoptionRequestForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    phone = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    message = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control", "rows": 4}))


class BankStatementForm(forms.ModelForm):
    class Meta:
        model = BankStatement
        fields = ["account_name", "period_start", "period_end", "opening_balance", "closing_balance", "file"]
        widgets = {
            "account_name": forms.TextInput(attrs={"class": "form-control"}),
            "period_start": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "period_end": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "opening_balance": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "closing_balance": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "file": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
