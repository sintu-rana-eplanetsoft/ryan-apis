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

@api_view(['GET'])
def testing_view(request):
    return Response('Testing')


# class ParcelDetailView(APIView):
#     def get(self, request, format=None):
#         address = request.query_params.get('address')
#         if not address:
#             return Response({"error": "Address parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        
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

#working

from django.conf import settings
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ParcelDetailView(APIView):
    def get(self, request, format=None):
        address = request.query_params.get('address')
        if not address:
            return Response({"error": "Address parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        regrid_api_key = "eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJyZWdyaWQuY29tIiwiaWF0IjoxNzIxOTc1NjIwLCJleHAiOjE3MjQ1Njc2MjAsInUiOjQzMDQ1MywiZyI6MjMxNTMsImNhcCI6InBhOnRzOnBzOmJmOm1hOnR5OmVvOnpvOnNiIn0.1_5YnmBlne8LGVNnXl16zyImmVEkc9RLYCdB20qzfHo"
        if not regrid_api_key:
            return Response({"error": "API key not found."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        base_url = os.getenv('BASE_URL')
        if not base_url:
            return Response({"error": "Base URL not found."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Replace spaces with %20 for URL encoding
        address = address.replace(' ', '%20')

        # Construct the API request URL using the base_url from .env
        url = f"{base_url}?query={address}&token={regrid_api_key}"

        # Send the API request
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "API request failed."}, status=response.status_code)





# import requests
# import json
# from pprint import pprint
# import folium
# import geopandas as gpd
# import matplotlib.pyplot as plt
# from shapely.geometry import Polygon, LineString
# from shapely.ops import transform
# from functools import partial
# import pyproj
# import warnings
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# warnings.filterwarnings("ignore")

# class ParcelImageView(APIView):
#     def get(self, request, format=None):
#         address = request.query_params.get('address')
#         if not address:
#             return Response({"error": "Address parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

#         regrid_api_key = "eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJyZWdyaWQuY29tIiwiaWF0IjoxNzE4MDEyODMxLCJleHAiOjE3MjA2MDQ4MzEsInUiOjQxMTU3MiwiZyI6MjMxNTMsImNhcCI6InBhOnRzOnBzOmJmOm1hOnR5OmVvOnpvOnNiIn0.GlLWQVnpvbr0zSs6Y733FmO0FomyBYa9jV5mP6f2dcQ"
#         url = f"https://app.regrid.com/api/v2/parcels/address?query={address}&token={regrid_api_key}"

#         response = requests.get(url)

#         if response.status_code == 200:
#             data = json.loads(response.text)
#             parcel = data["parcels"]["features"][0]["geometry"]["coordinates"][0]
#             building = data["buildings"]["features"][0]["geometry"]["coordinates"][0]

#             # Create a folium map centered at a specific location with satellite tiles
#             m = folium.Map(location=[32.835081, -96.5638745], zoom_start=19, tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr="Google Satellite")

#             # Convert the coordinates to the required format for folium
#             boundary = [[coord[1], coord[0]] for coord in parcel]
#             house = [[coord[1], coord[0]] for coord in building]

#             # Create a PolyLine connecting the boundary and house, and add it to the map
#             folium.PolyLine(locations=[boundary, house], color='blue', fill=True, fill_color='lightblue', fill_opacity=0.4).add_to(m)

#             # # Save the map to an HTML file
#             # map_file_path = 'map.html'
#             # m.save(map_file_path)

#             # Create GeoDataFrame for both parcels
#             parcel_polygon_1 = Polygon(building)
#             parcel_polygon_2 = Polygon(parcel)

#             parcel_gdf = gpd.GeoDataFrame(geometry=[parcel_polygon_1, parcel_polygon_2])

#             # Define the CRS for converting coordinates to inches (Web Mercator projection)
#             crs_meter = pyproj.CRS.from_epsg(3857)  # Web Mercator projection

#             # Conversion factor from meters to inches
#             METERS_TO_INCHES = 39.3701

#             # Function to calculate length of line in inches
#             def calculate_length_in_inches(line, crs):
#                 project = partial(
#                     pyproj.transform,
#                     pyproj.Proj(init='EPSG:4326'),  # WGS84
#                     pyproj.Proj(crs)
#                 )
#                 projected_line = transform(project, line)
#                 length_meters = projected_line.length
#                 length_inches = length_meters * METERS_TO_INCHES
#                 return length_inches

#             # Calculate dimensions of the parcels in inches
#             dimensions_inches = []
#             for parcel in parcel_gdf['geometry']:
#                 parcel_coords = list(parcel.exterior.coords)
#                 for i in range(len(parcel_coords) - 1):
#                     point1 = parcel_coords[i]
#                     point2 = parcel_coords[i + 1]
#                     line = LineString([point1, point2])
#                     length_inches = calculate_length_in_inches(line, crs_meter)
#                     dimensions_inches.append((line, length_inches))

#             # Plot the site plan
#             fig, ax = plt.subplots(figsize=(15, 15))

#             # Plot the parcels
#             parcel_gdf.plot(ax=ax, facecolor='white', alpha=0.5, edgecolor='blue', linewidth=1, label='Parcel')

#             # Annotate dimensions with arrows on the plot
#             for line, length in dimensions_inches:
#                 x_coords, y_coords = line.xy
#                 ax.plot(x_coords, y_coords, color='gray', linestyle='--', linewidth=1)  # Plot a dashed line for reference

#                 # Plot arrow at the end of the line
#                 ax.annotate("", xy=(x_coords[-1], y_coords[-1]), xytext=(x_coords[-2], y_coords[-2]),
#                             arrowprops=dict(arrowstyle="<|-|>", color='black', linestyle='--', linewidth=0.5))

#                 # Calculate midpoint for text annotation
#                 x_mid, y_mid = line.interpolate(0.5, normalized=True).xy

#                 # Annotate length below the line
#                 ax.annotate(f"{length:.2f}'", (x_mid[0], y_mid[0]), xytext=(0, -15),
#                             textcoords='offset points', ha='center', va='center', fontsize=10)

#             # Annotate "House (3893)" inside building
#             house_label_coords = parcel_polygon_1.representative_point().coords[0]
#             ax.annotate('House (3893 sqft)', (house_label_coords[0], house_label_coords[1]), ha='center', va='center', fontsize=10,
#                         bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='blue', lw=0.5))

#             # Annotate "Property Line" below parcel
#             property_line_coords = parcel_polygon_2.representative_point().coords[0]
#             ax.annotate('Property (9730 sqft)', (property_line_coords[0], property_line_coords[1] - 0.00003), ha='center', va='center', fontsize=10,
#                         bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='blue', lw=0.5))

#             ax.spines['top'].set_visible(False)
#             ax.spines['right'].set_visible(False)
#             ax.spines['left'].set_visible(False)
#             ax.spines['bottom'].set_visible(False)

#             ax.tick_params(axis='x', top=False, labeltop=False)  # Hide x-axis ticks and labels on top
#             ax.tick_params(axis='y', right=False, labelright=False)
#             ax.tick_params(axis='x', bottom=False, labelbottom=False)  # Hide x-axis ticks and labels on top
#             ax.tick_params(axis='y', left=False, labelleft=False)

#             # Set plot title and legend
#             plt.title('Site Plan')
#             plt.legend()

#             # pdf_file_path = 'site_plan.pdf'
#             # plt.savefig(pdf_file_path, format='pdf', bbox_inches='tight')

#             # Show plot
#             plt.show()

#             return Response({
#                 "status":True,
#                 "message": "Data retrieved and processed successfully.",
#             }, status=status.HTTP_200_OK)

#         else:
#             return Response({"error": "API request failed."}, status=response.status_code)

#working

import requests
import json
from pprint import pprint
import folium
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LineString
from shapely.ops import transform
from functools import partial
import pyproj
import warnings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

warnings.filterwarnings("ignore")

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from django.conf import settings
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import os
import json
import requests
import geopandas as gpd
import pyproj
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LineString
from shapely.ops import transform
from functools import partial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import os
import json
import requests
import geopandas as gpd
import pyproj
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LineString
from shapely.ops import transform
from functools import partial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ParcelImageView(APIView):
    def get(self, request, format=None):
        address = request.query_params.get('address')
        if not address:
            return Response({"error": "Address parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        regrid_api_key = "eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJyZWdyaWQuY29tIiwiaWF0IjoxNzIxOTc1NjIwLCJleHAiOjE3MjQ1Njc2MjAsInUiOjQzMDQ1MywiZyI6MjMxNTMsImNhcCI6InBhOnRzOnBzOmJmOm1hOnR5OmVvOnpvOnNiIn0.1_5YnmBlne8LGVNnXl16zyImmVEkc9RLYCdB20qzfHo"  # Make sure to replace this with your actual key
        if not regrid_api_key:
            return Response({"error": "API key not found."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        base_url = os.getenv('BASE_URL')
        if not base_url:
            return Response({"error": "Base URL not found."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        url = f"{base_url}?query={address}&token={regrid_api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            data = json.loads(response.text)
            parcel = data["parcels"]["features"][0]["geometry"]["coordinates"][0]
            building = data["buildings"]["features"][0]["geometry"]["coordinates"][0]

            parcel_polygon = Polygon(parcel)
            building_polygon = Polygon(building)

            parcel_gdf = gpd.GeoDataFrame(geometry=[building_polygon, parcel_polygon], crs="EPSG:4326")

            crs_meter = pyproj.CRS.from_epsg(3857)  # Web Mercator projection
            METERS_TO_INCHES = 39.3701

            def calculate_length_in_inches(line, src_crs, dst_crs):
                project = partial(
                    pyproj.Transformer.from_crs(src_crs, dst_crs, always_xy=True).transform
                )
                projected_line = transform(project, line)
                length_meters = projected_line.length
                length_inches = length_meters * METERS_TO_INCHES
                return length_inches

            dimensions_inches = []
            for parcel in parcel_gdf['geometry']:
                parcel_coords = list(parcel.exterior.coords)
                for i in range(len(parcel_coords) - 1):
                    point1 = parcel_coords[i]
                    point2 = parcel_coords[i + 1]
                    line = LineString([point1, point2])
                    length_inches = calculate_length_in_inches(line, pyproj.CRS("EPSG:4326"), crs_meter)
                    dimensions_inches.append((line, length_inches))

            fig, ax = plt.subplots(figsize=(15, 15))

            parcel_gdf.plot(ax=ax, facecolor='white', alpha=0.5, edgecolor='blue', linewidth=1, label='Parcel')

            # Annotate dimensions with arrows on the plot
            for line, length in dimensions_inches:
                x_coords, y_coords = line.xy
                ax.plot(x_coords, y_coords, color='gray', linestyle='--', linewidth=1)
                ax.annotate(
                    "",
                    xy=(x_coords[-1], y_coords[-1]),
                    xytext=(x_coords[-2], y_coords[-2]),
                    arrowprops=dict(arrowstyle="<|-|>", color='black', linestyle='--', linewidth=0.5)
                )
                x_mid, y_mid = line.interpolate(0.5, normalized=True).xy
                ax.annotate(
                    f"{length:.2f}'",
                    (x_mid[0], y_mid[0]),
                    xytext=(0, -15),
                    textcoords='offset points',
                    ha='center',
                    va='center',
                    fontsize=10,
                    color='black'
                )

            # Annotate "House (3893 sqft)" inside building
            house_label_coords = building_polygon.representative_point().coords[0]
            ax.annotate(
                'House (3893 sqft)',
                (house_label_coords[0], house_label_coords[1]),
                ha='center',
                va='center',
                fontsize=10,
                bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='blue', lw=0.5)
            )

            # Annotate "Property (9730 sqft)" below parcel
            property_label_coords = parcel_polygon.representative_point().coords[0]
            ax.annotate(
                'Property (9730 sqft)',
                (property_label_coords[0], property_label_coords[1] - 0.00003),
                ha='center',
                va='center',
                fontsize=10,
                bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='blue', lw=0.5)
            )

            # Label each vertex with 'a', 'b', 'c', etc.
            vertex_labels = 'abcdefghijklmnopqrstuvwxyz'
            for polygon in parcel_gdf['geometry']:
                coords = list(polygon.exterior.coords)
                for i, coord in enumerate(coords):
                    label = vertex_labels[i % len(vertex_labels)]  # Cycle through labels if more than 26 vertices
                    ax.annotate(
                        f'{label}',
                        (coord[0], coord[1]),
                        textcoords="offset points",
                        xytext=(0, 10),
                        ha='center',
                        fontsize=8,
                        color='black',
                        bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='blue', lw=0.5)
                    )

            # Label each edge with vertex labels (e.g., 'a-b', 'b-c', etc.)
            for polygon in parcel_gdf['geometry']:
                coords = list(polygon.exterior.coords)
                for i in range(len(coords) - 1):
                    start_label = vertex_labels[i % len(vertex_labels)]
                    end_label = vertex_labels[(i + 1) % len(vertex_labels)]
                    start_coord = coords[i]
                    end_coord = coords[i + 1]
                    midpoint = ((start_coord[0] + end_coord[0]) / 2, (start_coord[1] + end_coord[1]) / 2)
                    ax.annotate(
                        f'{start_label}-{end_label}',
                        midpoint,
                        textcoords="offset points",
                        xytext=(0, -15),
                        ha='center',
                        fontsize=8,
                        color='black',
                        bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='blue', lw=0.5)
                    )

            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['bottom'].set_visible(False)

            ax.tick_params(axis='x', top=False, labeltop=False)
            ax.tick_params(axis='y', right=False, labelright=False)
            ax.tick_params(axis='x', bottom=False, labelbottom=False)
            ax.tick_params(axis='y', left=False, labelleft=False)

            plt.title('Site Plan')
            plt.legend()

            plt.show()

            return Response({
                "status": True,
                "message": "Data retrieved and processed successfully.",
            }, status=status.HTTP_200_OK)

        else:
            return Response({"error": "API request failed."}, status=response.status_code)

