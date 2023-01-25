from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def pagina_de_prueba(request):
	return HttpResponse("<h1>Hola caracola</h1>");

def login(request):
	return HttpResponse(
