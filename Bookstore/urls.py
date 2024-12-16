from django.urls import path
from django.http import HttpResponse
from Bookstore.views import home, sobre

urlpatterns = [
    path("", home),
    path("sobre/", sobre),
]
