from django.urls import path
from app.views import *

urlpatterns = [
    path('dummy/',view_dummy,name='dummy'),
    path('parcel/', ParcelDetailView.as_view(), name='parcel-detail'),
]
