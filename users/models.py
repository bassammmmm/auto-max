from django.db import models
from django.contrib.auth.models import User
from localflavor.us.models import USStateField, USZipCodeField
from .utils import user_directory_path
from django.utils.safestring import mark_safe


User._meta.get_field('email')._unique = True #This is to make the Email attribute unique in the User Model.

class Location(models.Model):
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100, blank = True)
    state = USStateField(default='None')
    zip_code = USZipCodeField()
    
    def __str__(self):
        if hasattr(self, 'profile'):
            return f"Location {self.id} of profile {self.profile.user.username}"
        elif hasattr(self, 'listing'):
            return f"Location {self.id} of listing {self.listing.model} of profile {self.listing.seller.user.username}"
        else:
            return f"Location {self.id}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True)
    bio = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to = user_directory_path, null=True, default = 'default.png')
    phone_number = models.CharField(max_length=11, blank=True)

    @property
    def image_tag(self):
        return mark_safe(f"<img src = '{self.photo.url}' height = '50' />")
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    