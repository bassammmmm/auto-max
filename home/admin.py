from django.contrib import admin
from .models import Listing, LikedListing

# Register your models here.


class ListingAdmin(admin.ModelAdmin):
    list_filter = ['brand']
    search_fields = ['model']
    readonly_fields = ['id', 'vin', 'mileage', 'seller', 'color', 'model', 'brand', 'engine', 'location', 'image', 'description', 'transmission']
    

class LikedListingAdmin(admin.ModelAdmin):
    list_display = ['profile', 'listing']
    list_filter = ['profile']
    readonly_fields = ['id']
    search_fields = ['profile', 'listing']
    ordering = ['-date']

admin.site.register(Listing, ListingAdmin)

admin.site.register(LikedListing, LikedListingAdmin)
