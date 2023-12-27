from django import forms
from django.contrib.auth.models import User

from .models import Profile


''' Форма редактирования данных пользователя '''

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class ProfileEditForm(forms.ModelForm):

    data_of_brith = forms.DateField(label='дата рождения', widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Profile
        fields = ['data_of_brith', 'photo']

''' Форма регистрации пользователя '''

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Введите пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    username = forms.CharField(label='Логин', widget=forms.TextInput)
    email = forms.CharField(label='Почта', widget=forms.EmailInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Адрес электронной почты уже используется')
        return email

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']