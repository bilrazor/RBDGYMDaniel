from django.shortcuts import render
from django.http import HttpResponse , JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from .models import *
import json
from django.conf import settings
import uuid
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth import get_user
from django.contrib.auth.hashers import check_password

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
        if None in (nombre, correo, password, passwordConfirm):
            return JsonResponse({'error': 'Faltan parametros'}, status=400)
        # Validar que las contraseñas coincidan
        if password != passwordConfirm:
            return JsonResponse({'error': 'Las contraseñas no coinciden'}, status=400)
        
    
        # Validar que el usuario no exista
        if Tpersona.objects.filter(correo=correo).exists():
            return JsonResponse({'error': 'El usuario ya existe'}, status=409)

        # Crear el usuario
        user = Tpersona(nombre=nombre, correo=correo, password=password)
        user.set_password(password)
        user.save()

        # Crear y devolver el token de sesion
        # session_token = create_session_token(user)
        # user.session_token = session_token
        # user.save()
        # return JsonResponse({'sessionToken': session_token}, status=201)
        return JsonResponse({'OK': 'El usuario registrado'}, status=201)

    return HttpResponse(status=405)


@csrf_exempt
def sessions(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        correo = data.get('correo')
        password = data.get('password')
    
        if not all([correo, password]):
            return JsonResponse({'error': 'Parámetros faltantes: correo y password son requeridos'}, status=400)
        
        try:
            user = Tpersona.objects.get(correo=correo)
        except Tpersona.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=401)
        
        if check_password(password, user.password):
            session_token = uuid.uuid4()
            Tpersona.objects.filter(idpersona=user.idpersona).update(session_token=str(session_token))
            
            data = {'idpersona': user.idpersona, 'sessionToken': str(session_token)}
          
        else:
            return JsonResponse({'error': 'Contraseña incorrecta'}, status=401)
            
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
        session_token = request.headers.get('sessionToken')
        print(session_token)
        user = Tpersona.objects.get(idpersona=idpersona)
        
        if not session_token or session_token != user.session_token:
            return JsonResponse({"error": "Token de sesión inválido"}, status=401)
        
        data = {
            'dni': user.dni,
            'nombre':user.nombre,
            'correo': user.correo,
            'direccion': user.direccion,
            'telefono': user.telefono,
            'password':user.password
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
            
@csrf_exempt         
def datos(request, idpersona):

    if request.method == 'PUT':
# Recupera los datos enviados en la solicitud
        data = json.loads(request.body.decode("utf-8"))
# Recupera el usuario con idpersona
        try:
            user = Tpersona.objects.get(idpersona=idpersona)
        except Tpersona.DoesNotExist:
            return JsonResponse({'error': 'El usuario con idpersona {} no existe'.format(idpersona)}, status=400)
        # Actualiza los datos del usuario con los datos recibidos
 
        print(data.get("password"))
        print(data.get("nombre"))
        if data.get("nombre") != '':
            user.nombre = data.get("nombre")
        if data.get("correo") != '' :
            user.correo = data.get("correo") 
        if data.get("dni") != '' :
            user.dni = data.get("dni")
        if data.get("direccion") != '':    
            user.direccion = data.get("direccion")
        if data.get("telefono") != '':  
            user.telefono = data.get("telefono")
        if data.get("password") != '':  
            user.password = data.get("password")
            user.set_password(data.get("password"))
        print(user.nombre)
        print(user.correo)
        user.save()
        # Devuelve una respuesta vacía para indicar que la operación se realizó con éxito
        return JsonResponse({'mensaje': 'Perfil actualizado exitosamente'}, status=200)
    
"""   
@csrf_exempt
def datos(request, idpersona):
    if request.method == 'PUT':
        data = json.loads(request.body.decode("utf-8"))
        user = get_user(idpersona)
        if not user:
            return JsonResponse({'error': f'El usuario con idpersona {idpersona} no existe'}, status=400)
        update_user(user, data)
        return JsonResponse({'mensaje': 'Perfil actualizado exitosamente'}, status=200)

def get_user(idpersona):
    try:
        return Tpersona.objects.get(idpersona=idpersona)
    except Tpersona.DoesNotExist:
        return None

def update_user(user, data):
    user.nombre = data.get("nombre", user.nombre)
    user.correo = data.get("correo", user.correo)
    user.dni = data.get("dni", user.dni)
    user.direccion = data.get("direccion", user.direccion)
    user.telefono = data.get("telefono", user.telefono)
    password = data.get("password")
    if password:
        user.password = password
        user.set_password(password)
    user.save()"""