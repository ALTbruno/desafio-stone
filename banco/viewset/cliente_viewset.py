from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
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
		body = JSONParser().parse(request)
		serializer = ClienteSerializer(data=body)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

	if request.method == 'GET':
		query = Cliente.objects.all()
		serializer_class = ClienteSerializer(query, many=True)
	return JsonResponse(serializer_class.data, safe=False)

def buscar_cliente_por_id(request, id_cliente):
	if request.method == 'GET':
		query = Cliente.objects.get(pk=id_cliente)
		serializer_class = ClienteSerializer(query, many=False)
		return JsonResponse(serializer_class.data, safe=False)
