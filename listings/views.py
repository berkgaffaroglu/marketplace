from django.shortcuts import render
from .models import Listing
from rest_framework.response import Response
from rest_framework import status
from .serializers import ListingSerializer
from rest_framework.decorators import api_view, parser_classes,authentication_classes, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication



@api_view(['GET'])
def query_listings(request):
    listing_objects = Listing.objects.all().order_by('-created_at')
    pagination = PageNumberPagination()
    page = pagination.paginate_queryset(listing_objects, request)
    serializer = ListingSerializer(page, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def listing_detail(request, pk):
    # Get the listing object with a certain primary key.
    try:
        listing = Listing.objects.get(pk=pk)
    except Listing.DoesNotExist:
        return Response({"error": f"The listing with id:{pk} doesn't exist."}, status=status.HTTP_404_NOT_FOUND)
    serializer = ListingSerializer(listing)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([permissions.IsAuthenticated])
def create_listing(request):
    serializer = ListingSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    
@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([permissions.IsAuthenticated])
def edit_listing(request, pk):
    listing = Listing.objects.get(pk=pk)
    if listing.user.pk != request.user.pk:
        return Response({"error": "You do not have permission to edit this listing."}, status=status.HTTP_403_FORBIDDEN)
    serializer = ListingSerializer(listing, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()  # Use save() instead of update()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([permissions.IsAuthenticated])
def delete_listing(request, pk):
    try:
        listing = Listing.objects.get(pk=pk)
    except Listing.DoesNotExist:
        return Response({"error": f"The listing with the id:{pk} doesn't exist."}, status=status.HTTP_404_NOT_FOUND)
    
    if listing.user.pk != request.user.pk:
        return Response({"error": "You do not have permission to delete this listing."}, status=status.HTTP_403_FORBIDDEN)
    
    # If listing does exist, and the user has the permission to delete, delete it.
    listing.delete()
    return Response({"success": f"You successfully deleted the listing {pk}."}, status=status.HTTP_200_OK)