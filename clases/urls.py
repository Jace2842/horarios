from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import ClaseViewSet 

router = DefaultRouter()
router.register(r'api/clases', ClaseViewSet)
urlpatterns = [
    
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create_class/', views.create_class_view, name='create_class'),
    path('delete_class/', views.delete_class_view, name='delete_class'),
    path('modify_class/', views.modify_class_list, name='modify_class_list'),
    path('modify_class/<int:pk>/', views.modify_class, name='modify_class'),
    path('global_view/', views.global_view, name='global_view'),
    path('unauthorized/', views.unauthorized_view, name='unauthorized'),
    path('api/', include(router.urls)),

    path('mi-ubicacion/', views.mapa_ubicacion, name='mapa_ubicacion'),



]
