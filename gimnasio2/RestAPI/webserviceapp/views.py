from django.shortcuts import render
from django.http import HttpResponse , JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json
from django.conf import settings
import uuid
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
import datetime
from django.utils import timezone
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
        
        # Validar que la contraseña tenga al menos 8 caracteres
        if len(password) < 8:
            return JsonResponse({'error': 'La contraseña debe tener al menos 8 caracteres'}, status=400)
        # Validar que el correo sea de Gmail o Hotmail
        
        if not correo.endswith('@gmail.com') and not correo.endswith('@hotmail.com'):
            return JsonResponse({'error': 'El correo debe ser de Gmail o Hotmail'}, status=400)
        
        # Validar que el usuario no exista
        if Tpersona.objects.filter(correo=correo).exists():
            return JsonResponse({'error': 'El usuario ya existe'}, status=409)

        # Crear el usuario
        user = Tpersona(nombre=nombre, correo=correo, password=password)
        user.set_password(password)
        user.save()

      
        return JsonResponse({'OK': 'El usuario registrado'}, status=201)

    return HttpResponse(status=405)

 
    
@csrf_exempt
def sessions(request):
    #Verificar si el método de la petición es POST. Si no lo es, no hace nadaç
    
    if request.method == 'POST':
        
        #Carga los datos enviados en el cuerpo de la petición como un diccionario de 
        # Python utilizando json.loads(request.body).
        data = json.loads(request.body)
        
        #Obtiene los valores de "correo" y "password" del diccionario.
        correo = data.get('correo')
        password = data.get('password')
        #Verifica si ambos valores existen. Si alguno de ellos falta, devuelve una 
        # respuesta JSON con un error indicando que faltan parámetros.
        if not all([correo, password]):
            return JsonResponse({'error': 'Parámetros faltantes: correo y password son requeridos'}, status=400)
        #Intenta obtener un usuario de la base de datos con el correo especificado. 
        # Si el usuario no existe, devuelve  una respuesta JSON con un error indicando 
        # que el usuario no fue encontrado.
        try:
            user = Tpersona.objects.get(correo=correo)
        except Tpersona.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=401)
        #Verifica si la contraseña enviada coincide con la contraseña almacenada 
        # en la base de datos para ese usuario. Si no coincide, devuelve una respuesta JSON con un error indicando que la contraseña es incorrecta.
        if check_password(password, user.password):
            #Genera un token de sesión único y una fecha de expiración para ese token.
            session_token = uuid.uuid4()
            expires_at = datetime.datetime.now() + datetime.timedelta(minutes=1)            
            Tpersona.objects.filter(idpersona=user.idpersona).update(session_token=str(session_token), expires_at=expires_at)
            #Verifica si la fecha actual es mayor que la fecha de expiración. Si es así, devuelve una 
            # respuesta JSON con un error indicando que el token ha caducado.
            if datetime.datetime.now()  > expires_at:
                return JsonResponse({'error': 'Token ha caducado, inicia sesión de nuevo'}, status=401)        
            #Devuelve una respuesta JSON con los datos del usuario, incluyendo el ID de la 
            # persona, el token de sesión y la fecha de expiración.
            data = {'idpersona': user.idpersona, 'sessionToken': str(session_token), 'expiresAt': expires_at.isoformat()}
          
        else:
            return JsonResponse({'error': 'Contraseña incorrecta'}, status=401)
    
    
    return JsonResponse(data, status=200)
    


@csrf_exempt

def profile(request,idpersona):
        
    # La función verifica si la solicitud es de tipo GET.
    if request.method == 'GET':
        #Luego, obtiene el valor del encabezado "sessionToken" de la solicitud.
        session_token = request.headers.get('sessionToken')
        print(session_token)
        #Busca un objeto de la tabla Tpersona con el idpersona proporcionado en la URL.
        user = Tpersona.objects.get(idpersona=idpersona)
        #Verifica si el valor del encabezado "sessionToken" es válido comparándolo con el session_token almacenado en la tabla Tpersona.
        if not session_token or session_token != user.session_token:
            return JsonResponse({"error": "Token de sesión inválido"}, status=401)
        #Si el token de sesión es válido, se crea un diccionario con los datos del usuario (dni, nombre, correo, dirección, teléfono y contraseña).
        data = {
            'dni': user.dni,
            'nombre':user.nombre,
            'correo': user.correo,
            'direccion': user.direccion,
            'telefono': user.telefono,
            'password':user.password
        }
        #Finalmente, se devuelve una respuesta JSON con los datos del usuario.
        return JsonResponse(data)

 
            
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
 