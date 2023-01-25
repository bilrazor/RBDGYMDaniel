from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


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
		
	return JsonResponse(respuesta_final, safe=False);




    def users(request):
        correo = request.POST.get('correo')
        password = request.POST.get('password')
        if not correo or not password:
            return JsonResponse({'error': 'Email and password are required'}, status=400)
	
        
        # check if the email is already registered
        if User.objects.filter(correo=correo).exists():
            return JsonResponse({'error': 'Email already registered'}, status=400)
        
        # create a new user
        user = Tpersona.objects.create_user(nombre=nombre, correo=correo, password=password)
        user.save()
        
        # authenticate the user and log them in
        new_user = authenticate(correo=correo, password=password)
        login(request, new_user)
        
        return JsonResponse({'message': 'Registration successful'}, status=201);
