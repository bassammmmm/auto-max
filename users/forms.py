from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms



#TODO This if you wanna customize the django AuthenticationForm
class MyAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.widgets.TextInput(attrs={
                'style': 'background-color: #e6e6e6;'
            })
        self.fields['password'].widget = forms.widgets.PasswordInput(attrs={
                'style': 'background-color: #e6e6e6;'
            })
        
        
class ExtendedUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
