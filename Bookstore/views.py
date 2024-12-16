from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Teste Home")

def sobre(request):
    return HttpResponse("Teste Sobre")
