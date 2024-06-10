from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
import requests
import json

# Create your views here.

@api_view(['GET'])
def view_dummy(request):
    return Response({'status':True, 'data':'This is dummy API'})



# class ParcelDetailView(APIView):
#     def get(self, request, format=None):
#         address = request.query_params.get('address')
#         # if not address:
#         #     return Response({"error": "Address parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        
#         regrid_api_key = "eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJyZWdyaWQuY29tIiwiaWF0IjoxNzE4MDEyODMxLCJleHAiOjE3MjA2MDQ4MzEsInUiOjQxMTU3MiwiZyI6MjMxNTMsImNhcCI6InBhOnRzOnBzOmJmOm1hOnR5OmVvOnpvOnNiIn0.GlLWQVnpvbr0zSs6Y733FmO0FomyBYa9jV5mP6f2dcQ"
        
#         # Replace spaces with %20 for URL encoding
#         address = address.replace(' ', '%20')
#         base_url = "https://app.regrid.com/api/v2/parcels/address"
        
#         # Construct the API request URL
#         url = f"{base_url}?query={address}&token={regrid_api_key}"
        
#         # Send the API request
#         response = requests.get(url)
        
#         if response.status_code == 200:
#             data = response.json()
#             return Response(data, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "API request failed."}, status=response.status_code)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from drf_spectacular.utils import extend_schema, OpenApiParameter

class ParcelDetailView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(name='address', description='Address to search for parcels', required=True, type=str),
        ],
        responses={200: 'Application/JSON'},
    )
    def get(self, request, format=None):
        address = request.query_params.get('address')
        # if not address:
        #     return Response({"error": "Address parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        regrid_api_key = "eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJyZWdyaWQuY29tIiwiaWF0IjoxNzE4MDEyODMxLCJleHAiOjE3MjA2MDQ4MzEsInUiOjQxMTU3MiwiZyI6MjMxNTMsImNhcCI6InBhOnRzOnBzOmJmOm1hOnR5OmVvOnpvOnNiIn0.GlLWQVnpvbr0zSs6Y733FmO0FomyBYa9jV5mP6f2dcQ"

        # Replace spaces with %20 for URL encoding
        address = address.replace(' ', '%20')
        base_url = "https://app.regrid.com/api/v2/parcels/address"

        # Construct the API request URL
        url = f"{base_url}?query={address}&token={regrid_api_key}"

        # Send the API request
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "API request failed."}, status=response.status_code)