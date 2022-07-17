from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from banco.viewset import django_viewset
from banco.viewset.cliente_viewset import cliente_viewset
from banco.viewset.conta_viewset import ContaViewSet, get_saldo, depositar, sacar, transferir


router = routers.DefaultRouter()
router.register(r'users', django_viewset.UserViewSet)
router.register(r'groups', django_viewset.GroupViewSet)
router.register(r'contas', ContaViewSet, basename='Conta')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('contas/<int:id_conta>/saldo', get_saldo),
    path('contas/<int:id_conta>/depositar', depositar),
    path('contas/<int:id_conta>/sacar', sacar),
    path('contas/transferir', transferir),
    path('clientes/', cliente_viewset),
]
