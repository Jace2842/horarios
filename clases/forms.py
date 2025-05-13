from django import forms
from .models import Clase, Aula
from django.core.exceptions import ValidationError
from datetime import time, date

class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
        fields = ['nombre', 'descripcion', 'fecha', 'hora_inicio', 'hora_fin', 'aula', 'numero_alumnos']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora_inicio': forms.Select(),
            'hora_fin': forms.Select(),
            'aula': forms.Select(attrs={'onchange': 'actualizarCapacidad()'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Rellenamos las opciones de horas (6:00 a 22:30 cada 30 min)
        horas_disponibles = [
            (time(hour=h, minute=m).strftime("%H:%M"), time(hour=h, minute=m).strftime("%H:%M"))
            for h in range(6, 23) for m in (0, 30)
        ]
        self.fields['hora_inicio'].widget.choices = horas_disponibles
        self.fields['hora_fin'].widget.choices = horas_disponibles

        # Rellenamos aulas disponibles
        self.fields['aula'].queryset = Aula.objects.all()

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha < date.today():
            raise ValidationError('La fecha no puede ser menor a hoy.')
        return fecha

    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')
        aula = cleaned_data.get('aula')
        numero_alumnos = cleaned_data.get('numero_alumnos')

        # Validamos horas: la hora de fin debe ser mayor que la de inicio
        if hora_inicio and hora_fin:
            try:
                h_inicio = hora_inicio.hour * 60 + hora_inicio.minute
                h_fin = hora_fin.hour * 60 + hora_fin.minute
                if h_fin <= h_inicio:
                    raise ValidationError('La hora de fin debe ser mayor que la hora de inicio.')
            except ValueError:
                raise ValidationError('Formato de hora no válido.')

        # Validamos capacidad máxima del aula
        if aula and numero_alumnos:
            if numero_alumnos > aula.capacidad:
                self.add_error('numero_alumnos', f'El número de alumnos no puede ser mayor que la capacidad del aula ({aula.capacidad}).')