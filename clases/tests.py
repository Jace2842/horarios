from django.test import TestCase
from django.contrib.auth.models import User
from .models import Clase, Aula
from django.urls import reverse
from datetime import date, time
from django.contrib.auth.models import User


class ClaseModelTest(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username='usuario_test', password='password123')
        self.aula = Aula.objects.create(nombre="Aula 101", capacidad=30)
        self.clase = Clase.objects.create(
            user=self.usuario,  # corregido
            nombre="Matemáticas",
            descripcion="Clase de matemáticas básicas",
            fecha=date(2024, 5, 13),
            hora_inicio=time(10, 0),
            hora_fin=time(12, 0),
            aula=self.aula,
            numero_alumnos=25  # corregido
        )

    def test_clase_creation(self):
        self.assertEqual(self.clase.nombre, "Matemáticas")
        self.assertEqual(self.clase.aula.nombre, "Aula 101")
        self.assertEqual(self.clase.numero_alumnos, 25)

    def test_creacion_clase_valida(self):
        clase = Clase.objects.get(nombre="Matemáticas")
        self.assertEqual(clase.user.username, "usuario_test")


class ClaseViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_login_required_redirect(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, '/login/?next=/')
    
    def test_create_class_view_authenticated(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('create_class'))
        self.assertEqual(response.status_code, 200)