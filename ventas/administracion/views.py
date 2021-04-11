from django.shortcuts import render
from .models import Producto

# Create your views here.

def home(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
    return render(request, 'ventas/index.html', data)
def contacto(request):
    return render(request, 'ventas/contacto.html')
def galeria(request):
    return render(request, 'ventas/galeria.html')