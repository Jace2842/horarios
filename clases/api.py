from rest_framework import serializers
from .models import Clase

# clases/api.py
from rest_framework import viewsets
from .models import Clase
from .serializers import ClaseSerializer

class ClaseViewSet(viewsets.ModelViewSet):
    queryset = Clase.objects.all()
    serializer_class = ClaseSerializer

class ClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clase
        fields = '__all__'