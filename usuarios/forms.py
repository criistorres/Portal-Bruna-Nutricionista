from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm, SetPasswordForm
from .models import Users, Profile, Genero
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class UsersCreateForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'fone', 'data_nascimento')
        labels = {'username': 'Username/E-mail'}

    def __init__(self, *args, **kwargs):
        super(UsersCreateForm, self).__init__(*args, **kwargs)
        #Faz com que no formulario nao deixe alte
        # self.fields['email'].widget.attrs['readonly'] = True
        self.helper = FormHelper(self)
        self.helper.form_show_labels = True

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
        fields = ('first_name', 'last_name', 'email', 'fone', 'data_nascimento')

    def __init__(self, *args, **kwargs):
        super(UsersChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = True

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

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['foto', 'genero','is_paciente']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = True

class GeneroForm(forms.ModelForm):
    class Meta:
        model = Genero
        fields = ['nome','descricao']

    def __init__(self, *args, **kwargs):
        super(GeneroForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = True
