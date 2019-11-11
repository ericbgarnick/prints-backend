from django.urls import path

from photos import views

urlpatterns = [
    path(r'', views.PhotoCatalog.as_view())
]
