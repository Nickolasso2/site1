from cProfile import label
from django import forms
from .models import Category
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

class NewNews(forms.Form):
    title = forms.CharField(label='Заголовок новини', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    content = forms.CharField(
        label='Зміст новини', initial='поки що нічого не сталося', required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    is_published = forms.BooleanField(
        label='Відмітка про публікацію', initial=True)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), label='Категорія', empty_label='виберіть категорію', widget=forms.Select(attrs={'class': 'form-control'}))

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match('\d', title):
            raise ValidationError('error error')
        return title
        


class NewCategory(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']
        widgets = {'title': forms.TextInput(attrs={'class':'form-control'})}

class MyRegisterForm(UserCreationForm):
    email = forms.EmailField(label='e-mail',help_text='e-mail ьає бути дійсним' , widget=forms.EmailInput(attrs={'class':'form-control'}))
    username = forms.CharField(label='Користувач', widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Підтвердження паролю', widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        # doesn't work here so it is written down as redifining the attributes above
        # widgets = {'username': forms.TextInput(attrs={'class':'form-control'}), 'email': forms.EmailInput(attrs={'class':'form-control'}), 'password1': forms.PasswordInput(attrs={'class':'form-control'}), 'password2': forms.PasswordInput(attrs={'class':'form-control'})}

class MyLog_inForm(AuthenticationForm):
    username = forms.CharField(label='користувач')
    password = forms.CharField(label='пароль')



class SendMailForm(forms.Form):
    subj = forms.CharField(label='Тема', widget=forms.TextInput())
    conten = forms.CharField(label='Повідомлення', widget=forms.Textarea(attrs={'rows':5}))
    captcha = CaptchaField(label='Перевірка капча')