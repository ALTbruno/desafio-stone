import json
from pyexpat.errors import messages
from random import randrange
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from banco.model.transacao import Transacao

from banco.serializer.conta_serializer import ContaSerializer
from banco.model.conta import Conta

class ContaViewSet(viewsets.ReadOnlyModelViewSet):
	serializer_class = ContaSerializer
	queryset = Conta.objects.all()

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
