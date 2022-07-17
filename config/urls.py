from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from banco.viewset import django_viewset
from banco.viewset.cliente_viewset import ClienteViewSet
from banco.viewset.conta_viewset import Conta, ContaViewSet


router = routers.DefaultRouter()
router.register(r'users', django_viewset.UserViewSet)
router.register(r'groups', django_viewset.GroupViewSet)
router.register(r'clientes', ClienteViewSet, basename='Clientes')
router.register(r'contas', ContaViewSet, basename='Contas')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
