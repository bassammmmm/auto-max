from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from . models import *
from django.views import View
from .forms import *
from .filters import ListingFilter
from django.contrib import messages
from django.shortcuts import get_object_or_404


# Create your views here.

def main(request):
    return render(request, 'views/main.html')


@login_required
def home(request):
    current_user = request.user
    user_liked_listings = LikedListing.objects.filter(profile_id = current_user.profile.id).values_list('listing', flat = True) #.values_list returns list of tuples, pass flat = True for it to return list of values
    listings = Listing.objects.all().order_by('-created_at')
    listing_filter = ListingFilter(request.GET, queryset = listings)
    context = {
        'listing_filter' : listing_filter,
        'user_liked_listingsIDs' : user_liked_listings
        }
    return render(request, 'views/home.html', context)


class ListView(View):
    def get(self, request):
        listing_form = ListingForm()
        location_form = LocationForm()
        context = {
            'listing_form' : listing_form,
            'location_form' : location_form
        }
        return render(request, 'views/list.html', context)
    
    def post(self, request):
            listing_form = ListingForm(request.POST, request.FILES)
            location_form = LocationForm(request.POST)
            if listing_form.is_valid() and location_form.is_valid():
                listing = listing_form.save(commit=False)
                listing_location = location_form.save()
                listing.seller_id = request.user.profile.id
                listing.location = listing_location
                listing.save()
                messages.info(request, 'List created successfully!')
                return redirect('home')
            else:
                context = {
                    'listing_form' : listing_form,
                    'location_form' : location_form
                }
                return render(request, 'views/list.html', context)

            return redirect('home')
        
class ListDetailsView(View):
    def get(self, request, id):
        try:
            listing_details = Listing.objects.get(id=id)
            if listing_details is None:
                raise Exception
            return render(request, 'views/listing.html', {'listing' : listing_details})
        except Exception as e:
            messages.error(request, 'Something went wrong.')
            return redirect('home')


class ProfileView(View):
    
    def get(self, request):
        current_user = request.user
        user_form = UserForm(instance = current_user)
        profile_form = ProfileForm(instance = current_user.profile)
        location_form = LocationForm(instance = current_user.profile.location)
        user_listings = Listing.objects.filter(seller_id = current_user.profile.id)
        user_display_photo = current_user.profile.photo
        user_liked_listings = LikedListing.objects.filter(profile_id = current_user.profile.id)
        context = {
            'user_form' : user_form,
            'profile_form' : profile_form,
            'location_form' : location_form,
            'user_listings' : user_listings,
            'user_photo' : user_display_photo,
            'user_liked_listings' : user_liked_listings
        }
        return render(request, 'views/profile.html', context)
    
    def post(self, request):
        current_user = request.user
        user_form = UserForm(request.POST, instance = current_user)
        profile_form = ProfileForm(request.POST, request.FILES, instance = current_user.profile)
        location_form = LocationForm(request.POST, instance = current_user.profile.location)

        if user_form.is_valid() and profile_form.is_valid() and location_form.is_valid():
            user_form.save()
            profile_form.save()
            location_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
        else:
            user_listings = Listing.objects.filter(seller_id = current_user.profile.id)
            user_display_photo = current_user.profile.photo
            user_liked_listings = LikedListing.objects.filter(profile_id = current_user.profile.id)
            context = {
                'user_form' : user_form,
                'profile_form' : profile_form,
                'location_form' : location_form,
                'user_listings' : user_listings,
                'user_photo' : user_display_photo,
                'user_liked_listings' : user_liked_listings

            }
            return render(request, 'views/profile.html', context)
            
            
class EditListingView(View):
    def get(self, request, id):
        try:
            current_user = request.user
            global listing
            listing = Listing.objects.get(id = id, seller = current_user.profile)
            if listing is None:
                raise Exception
            listing_form = ListingForm(instance = listing)
            location_form = LocationForm(instance = listing.location)
            return render(request, 'views/edit.html', {'listing_form' : listing_form, 'location_form' : location_form})
        except Exception as e:
            messages.error(request, 'Something went wrong.')
            return redirect('home')
    def post(self, request, id):
        try:
            current_user = request.user
            global listing
            listing_form = ListingForm(request.POST, request.FILES, instance = listing)
            location_form = LocationForm(request.POST, instance = listing.location)
            if listing_form.is_valid() and location_form.is_valid():
                listing_form.save()
                location_form.save()
                messages.success(request, 'Listing data saved successfully!')
                return redirect('listing', id)
            else:
                return render(request, 'views/edit.html', {'listing_form' : listing_form, 'location_form' : location_form})
        except Exception as e:
            messages.error(request, 'Something went wrong.')
            return redirect('home')
    
    
class DeleteListingView(View):
    def get(self, request, id):
        user_listing = get_object_or_404(Listing, id = id, seller_id = request.user.profile.id)
        user_listing.delete()
        messages.success(request, 'Listing deleted successfully!')
        return redirect('home')

def like_listing(request, id):
        listing = get_object_or_404(Listing, id=id)
        current_user = request.user
        like_listing, created = LikedListing.objects.get_or_create(profile_id=current_user.profile.id, listing_id = listing.id)
        if created:
            like_listing.save()
        else:
            like_listing.delete()
        return JsonResponse({
            'is_liked' : created
        })