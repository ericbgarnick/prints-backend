from django.urls import path

from geospatial import views

urlpatterns = [
    path(r'meta', views.GeoSpatialMeta.as_view())
]
