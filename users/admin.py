from django.contrib import admin
from .models import *


class ProfileAdmin(admin.ModelAdmin):
    '''Admin View for ModelName'''

    list_display = ['user','image_tag', 'bio', ]


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Location)
