import json
from django.http import HttpResponse, JsonResponse
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


