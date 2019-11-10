from django.urls import path

from prints import views

urlpatterns = [
    path(r'meta', views.PrintsMeta.as_view())
]
