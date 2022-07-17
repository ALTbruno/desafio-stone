import datetime
import json
from random import randrange
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
	# if not Conta.objects.get(numero=numero_conta):
	conta = Conta(agencia='0001', numero=numero_conta, cliente=cliente)
	conta.save()

def get_saldo(request, id_conta):
	if request.method == 'GET':
		conta = Conta.objects.get(id=id_conta)
		saldo = conta.saldo
		return JsonResponse({'saldo': saldo})

@csrf_exempt
def depositar(request, id_conta):
	if request.method == 'POST':
		conta = Conta.objects.get(id=id_conta)
		data = json.loads(request.body.decode('utf-8'))
		valor_deposito = data['valor_deposito']
		saldo = conta.saldo
		saldo_atual = saldo + valor_deposito
		conta.saldo = saldo_atual
		transacao = Transacao()
		transacao.valor = valor_deposito
		transacao.tipo = Transacao.DEPOSITO
		transacao.conta = conta
		transacao.save()
		Conta.save(conta)
		return JsonResponse({'mensagem': 'Depósito realizado com sucesso.', 'saldo_anterior': saldo, 'saldo_atual': saldo_atual})

@csrf_exempt
def sacar(request, id_conta):
	if request.method == 'POST':
		conta = Conta.objects.get(id=id_conta)
		data = json.loads(request.body.decode('utf-8'))
		valor_saque = data['valor_saque']
		saldo = conta.saldo
		saldo_atual = saldo - valor_saque
		conta.saldo = saldo_atual
		transacao = Transacao()
		transacao.valor = valor_saque
		transacao.tipo = Transacao.SAQUE
		transacao.conta = conta
		transacao.save()
		Conta.save(conta)
		return JsonResponse({'mensagem': 'Saque realizado com sucesso.', 'saldo_anterior': saldo, 'saldo_atual': saldo_atual})

@csrf_exempt
def transferir(request):
	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))
		numero_conta_saida = data['conta_saida']
		numero_conta_destino = data['conta_destino']
		valor_transferencia = data['valor_transferencia']

		conta_saida = Conta.objects.get(numero=numero_conta_saida)
		conta_saida_saldo = conta_saida.saldo
		conta_destino = Conta.objects.get(numero=numero_conta_destino)
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

@csrf_exempt
def get_extrato(request, id_conta):
	if request.method == 'GET':
		query = Transacao.objects.filter(conta_id=id_conta)
		serializer_class = TransacaoSerializer(query, many=True)
		return JsonResponse(serializer_class.data, safe=False)