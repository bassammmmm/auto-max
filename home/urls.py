from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.main, name = 'main'),
    path('home/', views.home, name = 'home'),
    path('list/', login_required(views.ListView.as_view()), name = 'list'),
    path('listing-details/<str:id>', login_required(views.ListDetailsView.as_view()), name = 'listing'),
    path('profile/', login_required(views.ProfileView.as_view()), name = 'profile'),
    path('edit-listing/<str:id>', login_required(views.EditListingView.as_view()), name = 'edit'),
    path('delete-listing/<str:id>', login_required(views.DeleteListingView.as_view()), name = 'delete'),
    path('like-listing/<str:id>', views.like_listing, name = 'like_listing'),
]
