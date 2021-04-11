from django.urls import path
from administracion.views import home, contacto, galeria

urlpatterns = [
    path('', home, name="home"),
    path('contacto/', contacto, name="contacto"),
    path('galeria/', galeria, name="galeria"),
]