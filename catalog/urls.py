from django.urls import path

from catalog import views

urlpatterns = [
    path(r'', views.CatalogPhotos.as_view())
]
