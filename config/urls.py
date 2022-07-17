from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from banco.viewset import django_viewset
from banco.viewset.cliente_viewset import cliente_viewset, buscar_cliente_por_id
from banco.viewset.conta_viewset import get_saldo, depositar, sacar, transferir, get_extrato


router = routers.DefaultRouter()
router.register(r'users', django_viewset.UserViewSet)
router.register(r'groups', django_viewset.GroupViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('contas/<int:id_conta>/saldo', get_saldo),
    path('contas/<int:id_conta>/depositar', depositar),
    path('contas/<int:id_conta>/sacar', sacar),
    path('contas/<int:id_conta>/transacoes', get_extrato),
    path('contas/transferir', transferir),
    path('clientes/', cliente_viewset),
    path('clientes/<int:id_cliente>', buscar_cliente_por_id),
]
