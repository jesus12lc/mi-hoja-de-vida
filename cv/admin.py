from django.contrib import admin
from .models import (
    Perfil,
    Educacion,
    Experiencia,
    Habilidad,
    Certificado,
    Proyecto,
    Referencia,
    VentaGarage
)

# ================= ADMIN BASE CON VALIDACIÓN =================
class ValidatedAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.full_clean()  # Ejecuta las validaciones del models.py
        super().save_model(request, obj, form, change)

# ================= CONFIGURACIÓN DE INLINES =================
# Esto permite editar todo "amarrado" al perfil en una sola pantalla
class EducacionInline(admin.StackedInline):
    model = Educacion
    extra = 1

class ExperienciaInline(admin.StackedInline):
    model = Experiencia
    extra = 1

class HabilidadInline(admin.TabularInline): # Tabular ocupa menos espacio
    model = Habilidad
    extra = 1

# ================= PERFIL =================
@admin.register(Perfil)
class PerfilAdmin(ValidatedAdmin):
    list_display = ("nombres", "apellidos", "profesion", "email")
    search_fields = ("nombres", "apellidos")
    # Agregamos los Inlines aquí:
    inlines = [EducacionInline, ExperienciaInline, HabilidadInline]

# ================= RESTO DE MODELOS =================
# Se mantienen registrados por si quieres editarlos por separado

@admin.register(Educacion)
class EducacionAdmin(ValidatedAdmin):
    list_display = ("titulo", "institucion", "perfil")

@admin.register(Experiencia)
class ExperienciaAdmin(ValidatedAdmin):
    list_display = ("cargo", "empresa", "perfil")

@admin.register(Habilidad)
class HabilidadAdmin(ValidatedAdmin):
    list_display = ("nombre", "nivel", "perfil")

@admin.register(Certificado)
class CertificadoAdmin(ValidatedAdmin):
    list_display = ("titulo", "institucion", "perfil")

@admin.register(Proyecto)
class ProyectoAdmin(ValidatedAdmin):
    list_display = ("nombre", "tecnologias", "perfil")

@admin.register(Referencia)
class ReferenciaAdmin(ValidatedAdmin):
    list_display = ("nombre", "empresa", "perfil")

@admin.register(VentaGarage)
class VentaGarageAdmin(ValidatedAdmin):
    list_display = ("nombre_producto", "precio", "disponible", "perfil")
    list_filter = ("estado", "disponible")