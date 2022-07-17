from rest_framework import viewsets

from banco.serializer.cliente_serializer import ClienteSerializer
from banco.model.cliente import Cliente

class ClienteViewSet(viewsets.ModelViewSet):
	serializer_class = ClienteSerializer
	queryset = Cliente.objects.all()
