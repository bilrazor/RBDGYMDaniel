from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View


#models
from .models import Tpersona
# Create your views here.


def pagina_de_prueba(request):
	return HttpResponse("<h1>Hola caracola</h1>");

