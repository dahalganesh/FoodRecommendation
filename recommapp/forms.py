from django import forms
from .models import Customer
from django.contrib.auth.models  import User



class RegisterPageForm(forms.ModelForm):
    username= forms.CharField(widget=forms.TextInput())
    password= forms.CharField(widget=forms.PasswordInput())
    email= forms.CharField(widget=forms.EmailInput())
  
    class Meta:
        model = Customer
        fields = ['first_name','last_name','username','full_name', 'address',  'phone','email', 'password']

    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username = uname).exists():
            raise forms.ValidationError('this user name already exist')

        return uname



class LoginPageForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
