from django import forms
from . models import Listing
from users.models import Location, Profile
from django.contrib.auth.models import User
from localflavor.us.forms import USStateField, USZipCodeField
class ListingForm(forms.ModelForm):
    model = forms.CharField(label='Model', required=False)
    class Meta:
        model = Listing
        fields = ['brand', 'model', 'vin', 'mileage','color',  'engine', 'transmission', 'description','image']
        
        
        

class UserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, help_text="Username can't be changed.", ) # You can use: help_text, label, required, any many else to customize the form field
    first_name = forms.CharField(required=True, max_length=20)
    last_name = forms.CharField(required=True, max_length=20)
    email = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name'] 


class ProfileForm(forms.ModelForm):
    photo = forms.ImageField(widget=forms.FileInput(), label='New photo')
    class Meta:
        model = Profile
        fields = ['bio', 'phone_number', 'photo',]
 
class LocationForm(forms.ModelForm):
    zip_code = USZipCodeField(help_text='XXXXX or XXXXX-XXXX')
    class Meta:

        model = Location
        fields = ['address_1', 'address_2', 'state', 'zip_code']
