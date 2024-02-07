from django.db import models
# from django.contrib.auth.models import User
from accounts.models import AppUser as User

class Listing(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    def get_images(self):
        # Filtering all ListingImage objects related to this specific Listing
        return ListingImage.objects.filter(listing=self)
    def get_comments(self):
        # Filtering all ListingComments objects related to this specific Listing
        return ListingComment.objects.filter(listing=self)
    def __str__(self):
        # Returning Listing Primary Key for admin purposes.
        return "Listing: " + str(self.pk)


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='listing_images/')
    def __str__(self):
        return f"Image for the listing: {self.listing.pk}, {self.listing.title}"

class ListingComment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    comment = models.CharField(max_length = 300)
    def __str__(self):
        return f"Comment for the listing: {self.listing.pk}, {self.listing.title}"
    


