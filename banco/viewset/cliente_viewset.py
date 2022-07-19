import json
from django.db import transaction
from django.http import JsonResponse
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
@transaction.atomic
def cliente_viewset(request):
	if request.method == 'POST':
		body = json.loads(request.body.decode('utf-8'))
		serializer = ClienteSerializer(data=body)
		if serializer.is_valid():
			serializer.save()
			id = serializer.data.get('id')
			cliente = Cliente.objects.get(pk=id)
			abrir_conta(cliente)
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

	if request.method == 'GET':
		query = Cliente.objects.all()
		serializer_class = ClienteSerializer(query, many=True)
	return JsonResponse(serializer_class.data, safe=False)

def buscar_cliente_por_id(request, id_cliente):
	if request.method == 'GET':
		try:
			query = Cliente.objects.get(pk=id_cliente)
			serializer_class = ClienteSerializer(query, many=False)
			return JsonResponse(serializer_class.data, safe=False)
		except Cliente.DoesNotExist:
			return JsonResponse({"mensagem": "ID {} não encontrado.".format(id_cliente)}, status=400, safe=False)
