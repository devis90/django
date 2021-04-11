from django.contrib import admin

from .models import Empleado, Cliente, Rol, Producto, ProductoDetalle, Factura, Contacto, Vehiculo

# Register your models here.

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('numero_documento', 'tipo_documento', 'nombres', 'apellidos', 'telefono_celular' )
    search_fields = ( 'numero_documento', 'nombres', 'apellidos' )
    list_filter = ('tipo_documento',  'numero_documento' )
    ordering = ('apellidos','nombres',)
    fieldsets = (
        ('Información Personal', { 'fields': ('tipo_documento', 'numero_documento', 'nombres', 'apellidos', 'fechaNacimiento' ) } ),
        ('Información de contacto', { 'fields': ('telefono_casa', 'telefono_celular', 'direccion', 'correo' ) } ),
    )

class VehiculoAdmin(admin.ModelAdmin):    
    list_display = ('modelo', 'marca', 'observaciones', 'cliente')
    search_fields = ('modelo', 'marca', )
    list_filter = ('modelo', 'marca',)


admin.site.register(Empleado)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Rol)
admin.site.register(Producto)
admin.site.register(ProductoDetalle)
admin.site.register(Factura)
admin.site.register(Vehiculo, VehiculoAdmin)