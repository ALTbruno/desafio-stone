from rest_framework import viewsets

from banco.serializer.conta_serializer import ContaSerializer
from banco.model.conta import Conta

class ContaViewSet(viewsets.ModelViewSet):
	serializer_class = ContaSerializer
	queryset = Conta.objects.all()
