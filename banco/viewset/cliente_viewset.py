import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from django.views.decorators.csrf import csrf_exempt

from banco.serializer.cliente_serializer import ClienteSerializer
from banco.model.cliente import Cliente
from banco.viewset.conta_viewset import abrir_conta

# class ClienteViewSet(viewsets.ModelViewSet):
# 	serializer_class = ClienteSerializer
# 	queryset = Cliente.objects.all()
# 	# permission_classes = [permissions.IsAuthenticated]

@csrf_exempt
def cliente_viewset(request):
	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))
		cliente = Cliente()
		cliente.save()
		cliente.nome = data['nome']
		cliente.sobrenome = data['sobrenome']
		cliente.data_nascimento = data['data_nascimento']
		cliente.cpf = data['cpf']
		cliente.email = data['email']
		cliente.senha = data['senha']
		cliente.save()
		abrir_conta(cliente)
		return HttpResponse("Cliente cadastrado")

	if request.method == 'GET':
		query = Cliente.objects.all()
		serializer_class = ClienteSerializer(query, many=True)
		return JsonResponse(serializer_class.data, safe=False)

def buscar_cliente_por_id(request, id_cliente):
	if request.method == 'GET':
		query = Cliente.objects.get(pk=id_cliente)
		print(type(query))
		serializer_class = ClienteSerializer(query, many=False)
		return JsonResponse(serializer_class.data, safe=False)
