from django.shortcuts import render
from .models import Listing
from rest_framework.response import Response
from rest_framework import status
from .serializers import ListingSerializer
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser


@api_view(['GET'])
def all_listings(request):
    listing_objects = Listing.objects.all()
    serializer = ListingSerializer(listing_objects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def listing_detail(request, pk):
    # Filter the listing object with a certain primary key. Primary key's are
    # unique so this will always return one object or none. 
    listing_objects = Listing.objects.filter(pk=pk)
    serializer = ListingSerializer(listing_objects, many=True)
    # Since ListingSerializer returns a list, to return a single object, we get the first item on the list.
    return Response(serializer.data[0])


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def create_listing(request):
    serializer = ListingSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
    

# TODO
# @api_view(['POST'])
# @parser_classes([MultiPartParser, FormParser])
# def update_listing(request, pk):
#     serializer = ListingSerializer(data=request.data, context={'request': request})
#     if serializer.is_valid():
#         serializer.save()
#     else:
#         print(serializer.errors)
#     return Response(serializer.data)