from django.shortcuts import render
from django.http import HttpResponse , JsonResponse
from django.views.decorators.csrf import csrf_exempt

 
# Create your views here.
@csrf_exempt
def users(request):
    if request.method != 'POST':
        return None
       
       
    return JsonResponse({'status': 'ok'})
    


