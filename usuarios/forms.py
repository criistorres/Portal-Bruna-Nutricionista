from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Users

from django import forms

from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class UsersCreateForm(UserCreationForm):

    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'fone', 'data_nascimento')
        labels = {'username': 'Username/E-mail'}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["username"]
        if commit:
            user.save()
        return user


class UsersChangeForm(UserChangeForm):

    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'fone', 'data_nascimento')



class PasswordResetConfirmForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Redefinir Senha'))

    new_password1 = forms.CharField(
        label='Nova senha',
        widget=forms.PasswordInput,
    )

    new_password2 = forms.CharField(
        label='Confirme a nova senha',
        widget=forms.PasswordInput,
    )

