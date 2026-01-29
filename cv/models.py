from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime


class Perfil(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=50)
    lugar_nacimiento = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()

    cedula = models.CharField(max_length=10, unique=True)

    sexo = models.CharField(
        max_length=10,
        choices=[("Masculino", "Masculino"), ("Femenino", "Femenino"), ("Otro", "Otro")]
    )
    estado_civil = models.CharField(
        max_length=20,
        choices=[("Soltero", "Soltero"), ("Casado", "Casado"), ("Divorciado", "Divorciado"), ("Viudo", "Viudo")]
    )
    licencia_conducir = models.BooleanField(default=False)

    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    sitio_web = models.URLField(blank=True, null=True)

    direccion_domiciliaria = models.CharField(max_length=200)
    direccion_trabajo = models.CharField(max_length=200, blank=True, null=True)

    profesion = models.CharField(max_length=100)
    descripcion = models.TextField()

    foto = models.ImageField(upload_to="perfil/", blank=True, null=True)

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Datos Personales"

    def clean(self):
        super().clean()
        hoy = timezone.now().date()
        
        # Validación de fecha de nacimiento (Evita error NoneType)
        if self.fecha_nacimiento and self.fecha_nacimiento > hoy:
            raise ValidationError({"fecha_nacimiento": "La fecha de nacimiento no puede ser futura."})
        
        # Validación de cédula
        if self.cedula:
            if not self.cedula.isdigit() or len(self.cedula) != 10:
                raise ValidationError({"cedula": "La cédula debe contener exactamente 10 dígitos numéricos."})
        
        # Validación de teléfono
        if self.telefono:
            if not self.telefono.isdigit():
                raise ValidationError({"telefono": "El teléfono solo debe contener números."})

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class Educacion(models.Model):
    perfil = models.ForeignKey("cv.Perfil", on_delete=models.CASCADE, related_name="educaciones", null=True)
    institucion = models.CharField(max_length=150)
    titulo = models.CharField(max_length=150)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Educación"
        verbose_name_plural = "Educación"

    def clean(self):
        super().clean()
        hoy = timezone.now().date()
        
        if self.fecha_inicio and self.fecha_inicio > hoy:
            raise ValidationError({"fecha_inicio": "La fecha de inicio no puede ser futura."})
            
        if self.fecha_fin:
            if self.fecha_fin > hoy:
                raise ValidationError({"fecha_fin": "La fecha de fin no puede ser futura."})
            if self.fecha_inicio and self.fecha_inicio > self.fecha_fin:
                raise ValidationError("La fecha de inicio no puede ser mayor que la fecha de fin.")

    def __str__(self):
        return f"{self.titulo} - {self.institucion}"


class Experiencia(models.Model):
    perfil = models.ForeignKey("cv.Perfil", on_delete=models.CASCADE, related_name="experiencias", null=True)
    empresa = models.CharField(max_length=150)
    cargo = models.CharField(max_length=150)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    descripcion = models.TextField()

    class Meta:
        verbose_name = "Experiencia"
        verbose_name_plural = "Experiencias"

    def clean(self):
        super().clean()
        hoy = timezone.now().date()
        
        if self.fecha_inicio and self.fecha_inicio > hoy:
            raise ValidationError({"fecha_inicio": "La fecha de inicio no puede ser futura."})
            
        if self.fecha_fin:
            if self.fecha_fin > hoy:
                raise ValidationError({"fecha_fin": "La fecha de fin no puede ser futura."})
            if self.fecha_inicio and self.fecha_inicio > self.fecha_fin:
                raise ValidationError("La fecha de inicio no puede ser mayor que la fecha de fin.")

    def __str__(self):
        return f"{self.cargo} - {self.empresa}"


class Habilidad(models.Model):
    perfil = models.ForeignKey("cv.Perfil", on_delete=models.CASCADE, related_name="habilidades", null=True)
    nombre = models.CharField(max_length=100)
    nivel = models.IntegerField(help_text="Nivel del 1 al 10")

    class Meta:
        verbose_name = "Habilidad"
        verbose_name_plural = "Habilidades"

    def clean(self):
        super().clean()
        if self.nivel is not None:
            if self.nivel < 1 or self.nivel > 10:
                raise ValidationError({"nivel": "El nivel debe estar entre 1 y 10."})

    def __str__(self):
        return self.nombre


class Certificado(models.Model):
    perfil = models.ForeignKey("cv.Perfil", on_delete=models.CASCADE, related_name="certificados")
    titulo = models.CharField(max_length=200)
    institucion = models.CharField(max_length=200)
    fecha = models.DateField()
    imagen = models.ImageField(upload_to="certificados/")

    class Meta:
        verbose_name = "Certificado"
        verbose_name_plural = "Certificados"

    def clean(self):
        super().clean()
        hoy = timezone.now().date()
        if self.fecha and self.fecha > hoy:
            raise ValidationError({"fecha": "La fecha del certificado no puede ser futura."})

    def __str__(self):
        return self.titulo


class Proyecto(models.Model):
    perfil = models.ForeignKey("cv.Perfil", on_delete=models.CASCADE, related_name="proyectos")
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    tecnologias = models.CharField(max_length=300)
    github = models.URLField(blank=True, null=True)
    demo = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"

    def __str__(self):
        return self.nombre


class Referencia(models.Model):
    perfil = models.ForeignKey("cv.Perfil", on_delete=models.CASCADE, related_name="referencias", null=True)
    nombre = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        verbose_name = "Referencia"
        verbose_name_plural = "Referencias"

    def __str__(self):
        return f"{self.nombre} - {self.empresa}"


class VentaGarage(models.Model):
    perfil = models.ForeignKey("cv.Perfil", on_delete=models.CASCADE, related_name="ventas_garage")
    nombre_producto = models.CharField(max_length=150)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    estado = models.CharField(
        max_length=20,
        choices=[("Nuevo", "Nuevo"), ("Usado", "Usado")]
    )
    disponible = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to="venta_garage/", blank=True, null=True)
    fecha_publicacion = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Venta de Garage"
        verbose_name_plural = "Ventas de Garage"

    def clean(self):
        super().clean()
        if self.precio is not None and self.precio < 0:
            raise ValidationError({"precio": "El precio no puede ser negativo."})

    def __str__(self):
        return f"{self.nombre_producto} - ${self.precio}"