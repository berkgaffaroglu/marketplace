from django.urls import path
from .views import query_listings, listing_detail, create_listing
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('query-listings', query_listings, name='featured_listings'),
    path('listing-detail/<int:pk>', listing_detail, name='listing_detail'),
    path('create-listing', create_listing, name='create_listing')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)