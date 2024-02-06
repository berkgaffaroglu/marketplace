from django.contrib import admin
from .models import Listing, ListingImage, ListingComment

# Make ListingImage inline in admin to put it inside of ListingAdmin.
class ListingImageInline(admin.TabularInline):
    model = ListingImage

class ListingCommentInline(admin.TabularInline):
    model = ListingComment

class ListingAdmin(admin.ModelAdmin):
    inlines = [ListingCommentInline,ListingImageInline]

admin.site.register(Listing,ListingAdmin)
admin.site.register(ListingImage)