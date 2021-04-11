from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Producto(models.Model):
    codigo = models.CharField(verbose_name='Código', max_length=10)
    nombrep = models.CharField(verbose_name='Nombre de Producto', max_length=100)
    marcap = models.CharField(verbose_name='Marca de Producto', max_length=100)
    descripcionp = models.TextField(verbose_name='Descripción de Producto')
    valor = models.FloatField(verbose_name='Valor de Producto')
    imagen = models.ImageField(upload_to="productos", null=True)

    def __str__(self):
        return self.codigo


class ProductoDetalle(models.Model):
    cantidad = models.IntegerField()
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    valor_unitario = models.FloatField()
    valor_total = models.FloatField()

    def __str__(self):
        return str(self.cantidad)

class Rol(models.Model):
    nombre = models.CharField(max_length=10)
    descripcion = models.TextField()

    class Meta:
        verbose_name = 'Permisos'
        verbose_name_plural = 'Gestionar Roles'

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        permisos_defecto = ['add','change','delete','view']
        if not self.id:
            nuevo_grupo,creado = Group.objects.get_or_create(name=f'{self.nombre}')
            for permiso_temp in permisos_defecto:
                permiso, created = Permission.objects.update_or_create(
                    name = f'Can {permiso_temp} {self.nombre}',
                    content_type = ContentType.objects.get_for_model(Rol),
                    codename = f'{permiso_temp}_{self.nombre}'
                )
                if creado:
                    nuevo_grupo.permissions.add(permiso.id)
            super().save(*args,**kwargs)
        else:
            rol_antigo = Rol.objects.filter(id= self.id).values('nombre').first()
            if rol_antiguo['nombre'] == self.nombre:
                super().save(*args,**kwargs)
            else:
                Group.objects.filter(name= rol_antiguo['nombre']).update(name=f'{self.nombre}')
                for permiso_temp in permisos_defecto:
                    Permission.objects.filter(codename= f"{permiso_temp}_{rol_antiguo['nombre']}").update(
                        codename = f'{permiso_temp}_{self.nombre}',
                        name = f'Can {permiso_temp} {self.nombre}'
                    )
                super().save(*args,**kwargs)

class Persona(models.Model):
    TIPO_DOCUMENTO = [
        ('cedula', 'Cédula'),
        ('pasaporte', 'Pasaporte'),
        ('ruc', 'RUC'),
    ]
    nombres = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    tipo_documento = models.CharField(max_length=10, choices=TIPO_DOCUMENTO, default='cedula' )
    numero_documento = models.CharField(max_length=13)
    direccion = models.TextField(max_length=200)
    telefono_casa = models.CharField(max_length=10)
    telefono_celular = models.CharField(max_length=10)
    correo = models.EmailField()
    fechaNacimiento = models.DateTimeField('Fecha de nacimiento')

    class Meta:
        abstract = True

    def __str__(self):
        return self.nombres


class Empleado(Persona):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    correo_institucional = models.EmailField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo' )
    #foto = models.ImageField(verbose_name='Imagen de perfil',upload_to = 'imagenes/', blank=True, null=True, help_text=('Sube la fotografia tamaño carnet'))
    # relacion entre CLASES
    # uno a uno
    # muchos a uno
    # muchos a muchos
    # relacion con la clase user=> almacenar el usuario y contraseña.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.OneToOneField(Rol, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Gestionar Empleados'
        ordering = ['apellidos']

    def __str__(self):
        return self.nombres

class Cliente(Persona):
    
    def __str__(self):
        return self.nombres


def incremento_numero_factura():
    # consulta a la base de datos para saber cuantos registros se encuentran
    facturas = Factura.objects.all().order_by('id').last()
    if not facturas:
        return 'FAC0001'
    numero_factura = facturas.numero_factura
    int_factura = int(numero_factura.split('FAC')[-1])
    ancho = 4
    nuevo_numero_factura = int_factura + 1
    formatear = (ancho - len(str(nuevo_numero_factura))) * "0" + str(nuevo_numero_factura)
    n_numero_factura = 'FAC'+str(formatear)
    return n_numero_factura

class Factura(models.Model):
    # cedula, nombres, direccion, 
    ruc = models.CharField(max_length=13)
    numero_factura = models.CharField(verbose_name="Número de factura",max_length=20,default=incremento_numero_factura, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto_detalle = models.ManyToManyField(ProductoDetalle)
    subtotal = models.FloatField()
    descuento =models.FloatField()
    iva = models.FloatField()
    valor_final = models.FloatField()

    def __str__(self):
        return self.numero_factura


class Contacto(models.Model):
    nombres = models.CharField(verbose_name='Nombres y apellidos', max_length=200, blank=True, null=True)
    telefono = models.CharField(verbose_name='Telefono de contacto', max_length=15)
    email = models.EmailField(verbose_name='Correo  Electrónico', max_length=200, blank=True, null=True)
    consulta = models.TextField(verbose_name='Ingrese su consulta', blank=True, null=True)

    def __str__(self):
        return self.nombres

class Vehiculo(models.Model):
    marca = models.CharField(verbose_name='Marca', max_length=50)
    modelo = models.CharField(verbose_name='Modelo', max_length=50, blank=True, null=True)
    placa = models.CharField(verbose_name='Placa', max_length=7)
    color = models.CharField(verbose_name= 'Color de Vehiculo', max_length=50)
    kilometraje = models.IntegerField(verbose_name='Kilometraje') 
    observaciones = models.TextField(verbose_name= 'Descripción del problema')
    fechaIngreso = models.DateTimeField('Fecha de ingreso')
    cliente = models.ForeignKey(Cliente, on_delete= models.CASCADE)

    def __str__(self):
        return self.marca + ' ' + self.modelo + ' [ ' + self.observaciones + ' ] '