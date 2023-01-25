from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
#models
from .models import Tpersona
# Create your views here.


def pagina_de_prueba(request):
	return HttpResponse("<h1>Hola caracola</h1>");

def profile(request):
	datos = Tpersona.objects.all()
	respuesta_final = []
	for fila_sql in datos:
		diccionario = {}
		diccionario['nombre'] = fila_sql.nombre
		diccionario['correo'] = fila_sql.correo
		diccionario['password'] = fila_sql.password
		diccionario['direccion'] = fila_sql.direccion
		diccionario['telefono'] = fila_sql.telefono
		respuesta_final.append(diccionario)
		
	return JsonResponse(respuesta_final, safe=False)
