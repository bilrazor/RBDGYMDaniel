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
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth import get_user

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
            session_token = uuid.uuid4()
            Tpersona.objects.filter(idpersona=user.idpersona).update(session_token=session_token)
           
            data = {'idpersona': user.idpersona,'sessionToken': session_token}
         
        except Tpersona.DoesNotExist:
            return JsonResponse({'error': 'Usuario o contraseña incorrecto'}, status=401)
    return JsonResponse(data, status=200) 
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
  
 
"""  
@login_required
def profile(request):
    # Recuperar el token de sesión de la solicitud
    session_token = request.headers.get('sessionToken')
    # Verificar si el token de sesión es válido
    if session_token is None:
        return JsonResponse({"error": "Token de sesión inválido"}, status=401)
    # Recuperar el perfil del usuario autenticado
    user = request.user
    profile = {
        "Dni": user.dni,
        "nombre": user.nombre,
        "correo": user.correo,
        "direccion": user.direccion,
        "telefono": user.telefono
    }
    
    return JsonResponse(profile)
 
@login_required
def profile2(request):
    profile = Tpersona.objects.get(user=request.user)
    context = {
        'dni': profile.dni,
        'nombre': profile.nombre,
        'correo': profile.correo,
        'direccion': profile.direccion,
        'telefono': profile.telefono,
    }
    return render(request, 'user_profile.html', context)
""" 
"""
@csrf_exempt
def profile(request,idpersona):
    if request.method == 'GET':
        session_token = request.headers.get("sessionToken")
         if not session_token or session_token != token_en_la_bd:
            return JsonResponse({"error": "Token de sesión inválido"}, status=401)
        
        user = Tpersona.objects.get(idpersona=idpersona)
        if not session_token or session_token != user.session_token:
            return JsonResponse({"error": "Token de sesión inválido"}, status=401)
       
      
        data = {
        'dni': user.dni,
        'nombre':user.nombre,
        'correo': user.correo,
        'direccion': user.direccion,
        'telefono': user.telefono
    }
    
    return JsonResponse(data)"""

@csrf_exempt
def profile(request,idpersona):
    if request.method == 'GET':
        session_token = request.headers.get("sessionToken")
        
       
        user = Tpersona.objects.get(idpersona=idpersona)
        
        """if not session_token or session_token != user.session_token:
            return JsonResponse({"error": "Token de sesión inválido"}, status=401)"""
        
        data = {
            'dni': user.dni,
            'nombre':user.nombre,
            'correo': user.correo,
            'direccion': user.direccion,
            'telefono': user.telefono
        }
    
        return JsonResponse(data)


""" def profile(request):
    if request.method == 'GET':
        session_token = request.headers.get("sessionToken")
        idpersona = request.headers.get("IdPersona")
        
        try:
            # Validar sesión
            user = Tpersona.objects.get(idpersona=idpersona, session_token=session_token)
        except Tpersona.DoesNotExist:
            return JsonResponse({'error': 'Sesión inválida'}, status=401)
        
        try:
            persona = Tpersona.objects.get(idpersona=idpersona)
            data = {'nombre': persona.nombre, 'correo': persona.correo}
            return JsonResponse(data, status=200)
        except Tpersona.DoesNotExist:
            return JsonResponse({'error': 'La persona no existe'}, status=404)""" 