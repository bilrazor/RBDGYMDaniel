from django.shortcuts import render
from django.http import HttpResponse , JsonResponse
from .models import Tpersona

# Create your views here.

def paginaP(request):
    return HttpResponse("<h1>gHola</h1>");

def personas(request):
    lista = Tpersona.objects.all()
    respuesta_final = []
    for fila_sql in lista:
        diccionario = {}
        diccionario['nombre'] = fila_sql.nombre
        diccionario['correo'] = fila_sql.correo
        diccionario['telefono'] = fila_sql.telefono
    respuesta_final.append(diccionario)
    return JsonResponse(respuesta_final , safe=False);


   
def users(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        correo = request.POST['correo']
        password = request.POST['password']
        passwordConfirm = request.POST['passwordConfirm']
        if not correo or not password:
            return JsonResponse({'error': 'Email and password are required'}, status=400)
	
        
        # check if the email is already registered
        if Tpersona.objects.filter(correo=correo).exists():
            return JsonResponse({'error': 'Email already registered'}, status=400)
        
        # create a new user
        user = Tpersona.objects.create_user(nombre=nombre, correo=correo, password=password, passwordConfirm=passwordConfirm)
        user.save()
        
       
        return JsonResponse({'message': 'Registration successful'}, status=201); 
    


