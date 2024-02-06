from rest_framework import serializers
from .models import Listing
from .models import Listing, ListingImage, ListingComment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']

class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ['image']

class ListingCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ListingComment
        fields = '__all__'

class ListingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # Create an empty field for images. Then fill it with get_images function later.
    images = serializers.SerializerMethodField()

    # Create an empty field for comments. Then fill it with get_images function later.
    comments = serializers.SerializerMethodField()
    class Meta:
        model = Listing
        fields = '__all__'


    def create(self, validated_data):
        # When serializer.save() is called in views.py, get all images from the request
        images_data = self.context['request'].FILES.getlist('image')  # Access images from request.FILES

        # Create the listing first to get a listing object.
        listing = Listing.objects.create(**validated_data)

        # After getting the images 
        for image_data in images_data:
            ListingImage.objects.create(listing=listing, image=image_data)
        
        return listing
    
    def get_images(self, obj):
        images_queryset = ListingImage.objects.filter(listing=obj)
        images_serializer = ListingImageSerializer(images_queryset, many=True)
        return images_serializer.data

    def get_comments(self, obj):
        comments_queryset = ListingComment.objects.filter(listing=obj)
        comments_serializer = ListingCommentSerializer(comments_queryset, many=True)
        return comments_serializer.data