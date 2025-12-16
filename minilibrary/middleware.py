import time
from django.http import HttpResponseForbidden
from datetime import datetime
from django.shortcuts import redirect

BLOCKED_IPS = ["127.0.0.1"]
EXCEPT_URLS = ['/login/','/admin/', '/register/']

class TimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        start = time.time()
        
        response = self.get_response(request)
        
        duration = time.time() - start
        print(f"Tiempo de respuesta: {duration:.2f} segundos")
        return response
    
class BlockIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR")
        print(f"IP detectada: {ip}")
        
        
        if ip in BLOCKED_IPS:
            return HttpResponseForbidden("Tu IP está bloqueada")
        
        return self.get_response(request)
    
class OfficeHoursOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        now = datetime.now()
        
        if now.hour < 8 or now.hour > 18:
            return HttpResponseForbidden(f"No es horario de oficina")
         
        return self.get_response(request)
    
class RequireLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        
        if not request.user.is_authenticated and not any(request.path.startswith(url) for url in EXCEPT_URLS):
            print("Usuario no autenticado, redirigiendo...")
            return redirect('/admin/')
        
        return self.get_response(request)