from django.shortcuts import render
from .models import Perfil # Solo necesitamos importar Perfil para acceder a lo demás

def cv_view(request):
    # Obtenemos el perfil principal
    perfil = Perfil.objects.first()

    # Si no existe un perfil, enviamos contexto básico para evitar errores en el template
    if not perfil:
        return render(request, 'cv/cv.html', {'perfil': None})

    # Construimos el contexto usando las relaciones inversas (related_name)
    # Esto asegura que los datos mostrados estén "amarrados" a este perfil
    context = {
        'perfil': perfil,
        
        # Listados ordenados por fecha a través del perfil
        'educaciones': perfil.educaciones.all().order_by('-fecha_inicio'),
        'experiencias': perfil.experiencias.all().order_by('-fecha_inicio'),
        
        # Listados simples relacionados
        'habilidades': perfil.habilidades.all(),
        'certificados': perfil.certificados.all(),
        'proyectos': perfil.proyectos.all(),
        'referencias': perfil.referencias.all(),
        
        # Filtramos las ventas de garage disponibles de este perfil
        'ventas': perfil.ventas_garage.filter(disponible=True)
    }

    return render(request, 'cv/cv.html', context)


def home(request):
    perfil = Perfil.objects.first()
    return render(request, 'cv/home.html', {'perfil': perfil})