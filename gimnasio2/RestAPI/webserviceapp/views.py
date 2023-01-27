from django.shortcuts import render
from django.http import HttpResponse , JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from .models import *
import json
import datetime
from django.conf import settings
import hashlib 

# Create your views here.
@csrf_exempt
def users(request):
    data = json.loads(request.body)
    if request.method == 'POST':
        nombre = data.get('nombre')
        correo = data.get('correo')
        password = data.get('password')
        passwordConfirm = data.get('passwordConfirm')

        # Validar que todos los campos esten completos
        if not all([nombre, correo, password, passwordConfirm]):
            return JsonResponse({'error': 'Faltan parámetros'}, status=400)

        # Validar que las contraseñas coincidan
        if password != passwordConfirm:
            return JsonResponse({'error': 'Las contraseñas no coinciden'}, status=400)

        # Validar que el usuario no exista
        if Tpersona.objects.filter(correo=correo).exists():
            return JsonResponse({'error': 'El usuario ya existe'}, status=409)

        # Crear el usuario
        user = Tpersona(nombre=nombre, correo=correo, password=password)
        user.save()

        # Crear y devolver el token de sesion
        # session_token = create_session_token(user)
        # user.session_token = session_token
        # user.save()
        # return JsonResponse({'sessionToken': session_token}, status=201)
        return JsonResponse({'OK': 'El usuario registrado'}, status=200)

    return HttpResponse(status=405)


 
@csrf_exempt
def sessions(request):
    if request.method != 'POST':
        return HttpResponse(status=405)
    
    data = json.loads(request.body)
    correo = data.get('correo')
    password = data.get('password')
    
    if not all([correo, password]):
        return JsonResponse({'error': 'Faltan parámetros'}, status=400)
    
    user = Tpersona.objects(correo=correo, password=password)
    user = authenticate(correo=correo, password=password)
    if user is None:
        return JsonResponse({'error': 'Credenciales inválidas'}, status=401)
    
    login(request, user)
    
    session_token = create_session_token(user)
    return JsonResponse({'session_token': session_token}, status=200)


def create_session_token(user):
    # Crear una instancia del algoritmo sha256
    sha = hashlib.sha256()
    # Agregar el nombre de usuario y el ID como salt
    sha.update((user.correo + str(user.id)).encode('utf-8'))
    # Devolver el token encriptado
    return sha.hexdigest()
