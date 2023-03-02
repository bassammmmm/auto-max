from django.contrib import admin
from .models import Listing, LikedListing

# Register your models here.


class ListingAdmin(admin.ModelAdmin):
    list_filter = ['brand']
    search_fields = ['model']
    
    

class LikedListingAdmin(admin.ModelAdmin):
    list_display = ['profile', 'listing']
    list_filter = ['profile']
    readonly_fields = ['id']
    search_fields = ['profile', 'listing']
    ordering = ['-date']

admin.site.register(Listing, ListingAdmin)

admin.site.register(LikedListing, LikedListingAdmin)
