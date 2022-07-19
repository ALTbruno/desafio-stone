import datetime
import json
from decimal import Decimal
from random import randrange
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from banco.model.transacao import Transacao

from banco.serializer.conta_serializer import ContaSerializer
from banco.model.conta import Conta
from banco.serializer.transacao_serializer import TransacaoSerializer

# class ContaViewSet(viewsets.ReadOnlyModelViewSet):
# 	serializer_class = ContaSerializer
# 	queryset = Conta.objects.all()

def gerar_numero():
	return randrange(1000000000,9000000000)

def abrir_conta(cliente):
	numero_conta = gerar_numero()
	while(Conta.objects.filter(numero=numero_conta).exists()):
		numero_conta = gerar_numero()
	conta = Conta(agencia='0001', numero=numero_conta, cliente=cliente)
	conta.save()

def get_saldo(request, id_conta):
	if request.method == 'GET':
		try:
			conta = Conta.objects.get(pk=id_conta)
			saldo = conta.saldo
			return JsonResponse({'saldo': saldo}, safe=False)
		except Conta.DoesNotExist:
			return JsonResponse({"mensagem": "ID {} não encontrado.".format(id_conta)}, status=400, safe=False)

@csrf_exempt
def depositar(request, id_conta):
	if request.method == 'POST':
		try:
			conta = Conta.objects.get(id=id_conta)
			data = json.loads(request.body.decode('utf-8'))
			valor_deposito = Decimal(data['valor_deposito'])
			saldo = conta.saldo
			saldo_atual = saldo + valor_deposito
			conta.saldo = saldo_atual
			transacao = Transacao()
			transacao.valor = valor_deposito
			transacao.data_hora = datetime.datetime.now()
			transacao.tipo = Transacao.DEPOSITO
			transacao.conta = conta
			transacao.save()
			Conta.save(conta)
			return JsonResponse({'mensagem': 'Depósito realizado com sucesso.', 'saldo_anterior': saldo, 'saldo_atual': saldo_atual})
		except Conta.DoesNotExist:
			return JsonResponse({"mensagem": "ID {} não encontrado.".format(id_conta)}, status=400, safe=False)

@csrf_exempt
def sacar(request, id_conta):
	if request.method == 'POST':
		try:
			conta = Conta.objects.get(id=id_conta)
			data = json.loads(request.body.decode('utf-8'))
			valor_saque = Decimal(data['valor_saque'])
			saldo = conta.saldo
			saldo_atual = saldo - valor_saque
			conta.saldo = saldo_atual
			transacao = Transacao()
			transacao.valor = valor_saque
			transacao.data_hora = datetime.datetime.now()
			transacao.tipo = Transacao.SAQUE
			transacao.conta = conta
			transacao.save()
			Conta.save(conta)
			return JsonResponse({'mensagem': 'Saque realizado com sucesso.', 'saldo_anterior': saldo, 'saldo_atual': saldo_atual})
		except Conta.DoesNotExist:
			return JsonResponse({"mensagem": "ID {} não encontrado.".format(id_conta)}, status=400, safe=False)

@csrf_exempt
@transaction.atomic
def transferir(request):
	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))
		numero_conta_saida = data['conta_saida']
		numero_conta_destino = data['conta_destino']
		valor_transferencia = Decimal(data['valor_transferencia'])

		if numero_conta_saida == numero_conta_destino:
			return JsonResponse({"mensagem": "A conta de destino deve ser diferente da conta de saida"}, status=400, safe=False)

		try:
			conta_saida = Conta.objects.get(numero=numero_conta_saida)
		except Conta.DoesNotExist:
			return JsonResponse({"mensagem": "Conta {} não encontrada.".format(numero_conta_saida)}, status=400, safe=False)
		try:
			conta_destino = Conta.objects.get(numero=numero_conta_destino)
		except Conta.DoesNotExist:
			return JsonResponse({"mensagem": "Conta {} não encontrada.".format(numero_conta_destino)}, status=400, safe=False)
		
		conta_saida_saldo = conta_saida.saldo

		if valor_transferencia > conta_saida_saldo:
			return JsonResponse({"mensagem": "Saldo insuficiente"}, status=400, safe=False)

		conta_destino_saldo = conta_destino.saldo
		conta_saida_saldo_atual = conta_saida_saldo - valor_transferencia
		conta_destino_saldo_atual = conta_destino_saldo + valor_transferencia

		conta_saida.saldo = conta_saida_saldo_atual
		conta_destino.saldo = conta_destino_saldo_atual

		data_hora_atual = datetime.datetime.now()

		transacao_saida = Transacao()
		transacao_saida.valor = valor_transferencia
		transacao_saida.data_hora = data_hora_atual
		transacao_saida.tipo = Transacao.TRANSFERENCIA_ENVIADA
		transacao_saida.conta = conta_saida
		transacao_saida.save()

		transacao_entrada = Transacao()
		transacao_entrada.valor = valor_transferencia
		transacao_entrada.data_hora = data_hora_atual
		transacao_entrada.tipo = Transacao.TRANSFERENCIA_RECEBIDA
		transacao_entrada.conta = conta_destino
		transacao_entrada.save()

		Conta.save(conta_saida)
		Conta.save(conta_destino)
		return JsonResponse({'mensagem': 'Transferência realizada com sucesso.'})

def get_extrato(request, id_conta):
	if request.method == 'GET':
		query = Transacao.objects.filter(conta_id=id_conta).order_by('-data_hora')
		De = request.GET.get('De', None)
		Ate = request.GET.get('Ate', None)
		if De and Ate:
			query = query.filter(conta_id=id_conta, data_hora__range=[De, Ate])
		serializer_class = TransacaoSerializer(query, many=True)
		return JsonResponse(serializer_class.data, safe=False)

def listar_contas(request):
	if request.method == 'GET':
		query = Conta.objects.all()
		serializer_class = ContaSerializer(query, many=True)
		return JsonResponse(serializer_class.data, safe=False)

def buscar_conta_por_id(request, id_conta):
	if request.method == 'GET':
		try:
			query = Conta.objects.get(pk=id_conta)
			serializer_class = ContaSerializer(query, many=False)
			return JsonResponse(serializer_class.data, safe=False)
		except Conta.DoesNotExist:
			return JsonResponse({"mensagem": "ID {} não encontrado.".format(id_conta)}, status=400, safe=False)

