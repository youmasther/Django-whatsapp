from django import forms
# from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm
from PIL import Image
from django.forms import fields
from .models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'prenom', 'nom', 'image')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'prenom', 'nom', 'image', 'password', 'is_superuser', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]

class UserCreationForm2(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'prenom', 'nom',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ProfileImageUpdateForm(forms.ModelForm):
    """Cette class permet de modifier seulement l'image de profile 
    de l'utilisateur connecté"""
    class Meta:
        model = User
        fields = ('image',)

class UpdateUserForm(forms.ModelForm):
    """Cette class permet de modifier les informations de l'utilisateur"""
    class Meta:
        model = User
        fields = ('email', 'prenom', 'nom',)


# The `PasswordChangeFormEdit` class extends `PasswordChangeForm` and customizes the appearance of the
# password change form fields.
class PasswordChangeFormEdit(PasswordChangeForm):
    """
    The `PasswordChangeFormEdit` class extends `PasswordChangeForm` and customizes the appearance of the
    password change form fields.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class' : 'form-control mb-2','placeholder':'Votre ancien mot de passe'})
        self.fields['new_password1'].widget.attrs.update({'class' : 'form-control mb-2','placeholder':'Votre nouveau mot de passe'})
        self.fields['new_password2'].widget.attrs.update({'class' : 'form-control mb-2','placeholder':'confirmer votre mot de passe '})