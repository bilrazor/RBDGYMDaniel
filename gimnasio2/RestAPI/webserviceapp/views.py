from django.shortcuts import render
from django.http import HttpResponse , JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from .models import *
import json
import datetime
from django.conf import settings
import hashlib 
import uuid

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
    if request.method == 'POST':
        data = json.loads(request.body)
        correo = data.get('correo')
        password = data.get('password')
    
        if not all([correo, password]):
            return JsonResponse({'error': 'Faltan parámetros'}, status=400)
        try:
            user = Tpersona.objects.get(correo=correo, password=password)
            user.save()
        except Tpersona.DoesNotExist:
            return JsonResponse({'error': 'Usuario o contraseña incorrecto'}, status=401)
         
      
        #generate session token
        session_token = uuid.uuid4()
         
    return JsonResponse({'session_token': uuid.uuid4()}, status=200)


 #@csrf_exempt
#def sessions(request):
 #   if request.method == 'POST':
  #      data = json.loads(request.body)
  #      correo = data.get('correo')
  #      password = data.get('password')
#
 #       user = authenticate(request, correo=correo, password=password)
 #       if user is None:
 #           return JsonResponse({'error': 'Credenciales inválidas'}, status=401)
 #       login(request, user)

        #generate session token
#        session_token = uuid.uuid4()
#
 #       return JsonResponse({'session_token': str(session_token)}, status=200)
  #  else:
  #      return JsonResponse({'error': 'Método no permitido'}, status=405)