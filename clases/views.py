from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Clase
from .forms import ClaseForm
from datetime import timedelta, datetime
import json
from .models import Aula
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

# Función para obtener datos del clima desde OpenMeteo
def fetch_clima_open_meteo(lat, lon):
    """Fetch weather data from Open-Meteo API"""
    url = f"https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m"],
        "timezone": "auto"
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()  # Lanzará una excepción si hay error HTTP
    return response.json()

# Vista para el mapa y clima
def mapa(request):
    """Vista para mostrar el mapa con la ubicación del usuario"""
    return render(request, 'mapa.html')

# Endpoint para obtener clima - acepta GET y POST
@csrf_exempt
def obtener_clima(request):
    if request.method == "POST":
        try:
            payload = json.loads(request.body)
            lat = payload.get("latitude")
            lon = payload.get("longitude")
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)
    elif request.method == "GET":
        lat = request.GET.get("latitude")
        lon = request.GET.get("longitude")
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    if lat is None or lon is None:
        return JsonResponse({"error": "Coordenadas no válidas"}, status=400)
    
    try:
        datos = fetch_clima_open_meteo(lat, lon)
        return JsonResponse(datos, status=200)
    except requests.exceptions.HTTPError as http_err:
        return JsonResponse(
            {"error": f"Error HTTP al obtener clima: {http_err}"}, status=502
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    clases = Clase.objects.filter(user=request.user)
    horario = []
    start = datetime.strptime('00:00', '%H:%M')
    for i in range(48):
        bloque = (start + timedelta(minutes=30*i)).strftime('%H:%M')
        horario.append(bloque)
    return render(request, 'home.html', {'clases': clases, 'horario': horario})

@login_required
def create_class_view(request):
    aulas = Aula.objects.all()
    aulas_json = json.dumps(list(aulas.values('id', 'nombre', 'capacidad')), cls=DjangoJSONEncoder)

    if request.method == 'POST':
        form = ClaseForm(request.POST)
        if form.is_valid():
            clase = form.save(commit=False)
            clase.user = request.user
            clase.save()
            return redirect('home')
    else:
        form = ClaseForm()
    return render(request, 'create_class.html', {'form': form, 'aulas_json': aulas_json})


@login_required
def delete_class_view(request):
    clases = Clase.objects.filter(user=request.user)
    if request.method == 'POST':
        clase_id = request.POST.get('clase_id')
        clase = get_object_or_404(Clase, id=clase_id, user=request.user)
        clase.delete()
        return redirect('delete_class')
    return render(request, 'delete_class.html', {'clases': clases})

@login_required
def modify_class_list(request):
    clases = Clase.objects.filter(user=request.user)
    return render(request, 'modify_class_list.html', {'clases': clases})

@login_required
def modify_class(request, pk):
    clase = get_object_or_404(Clase, pk=pk, user=request.user)
    aulas = Aula.objects.all()
    aulas_json = json.dumps(list(aulas.values('id', 'nombre', 'capacidad')), cls=DjangoJSONEncoder)

    if request.method == 'POST':
        form = ClaseForm(request.POST, instance=clase)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ClaseForm(instance=clase)
    return render(request, 'modify_class.html', {'form': form, 'aulas_json': aulas_json})

@login_required
def global_view(request):
    aulas = Aula.objects.all()
    clases = None
    selected_aula = None
    selected_date = None

    if request.method == 'POST':
        aula_id = request.POST.get('aula')
        fecha = request.POST.get('fecha')
        selected_aula = get_object_or_404(Aula, pk=aula_id)
        selected_date = fecha
        clases = Clase.objects.filter(aula=selected_aula, fecha=fecha).order_by('hora_inicio')

    return render(request, 'global_view.html', {
        'aulas': aulas,
        'clases': clases,
        'selected_aula': selected_aula,
        'selected_date': selected_date,
    })

def unauthorized_view(request):
    return render(request, 'unauthorized.html')