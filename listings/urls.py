from django.urls import path
from .views import query_listings, listing_detail, create_listing, edit_listing, delete_listing

from django.conf.urls.static import static

urlpatterns = [
    path('query-listings', query_listings, name='featured_listings'),
    path('listing-detail/<int:pk>', listing_detail, name='listing_detail'),
    path('create-listing', create_listing, name='create_listing'),
    path('edit-listing/<int:pk>', edit_listing, name='edit_listing'),
    path('delete-listing/<int:pk>', delete_listing, name='delete_listing')
]
