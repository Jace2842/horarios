from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import ClaseViewSet
# urls.py
from django.urls import path
from . import views


router = DefaultRouter()
router.register(r'api/clases', ClaseViewSet)


urlpatterns = [
    path('', views.login_view, name='login_root'),  # Keep this for the root URL
    path('login/', views.login_view, name='login'),  # Add this for the /login/ URL
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('create_class/', views.create_class_view, name='create_class'),
    path('delete_class/', views.delete_class_view, name='delete_class'),
    path('modify_class_list/', views.modify_class_list, name='modify_class_list'),
    path('modify_class/<int:pk>/', views.modify_class, name='modify_class'),
    path('global_view/', views.global_view, name='global_view'),
    path('unauthorized/', views.unauthorized_view, name='unauthorized'),
    path('mapa/', views.mapa, name='mapa'),
    path('api/clima/', views.obtener_clima, name='obtener_clima'),
]
