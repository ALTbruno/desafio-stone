from tkinter import CASCADE
from django.db import models

from banco.model.conta import Conta

class Transacao(models.Model):

	DEPOSITO = 'DPST'
	SAQUE = 'SQUE'
	TRANSFERENCIA_RECEBIDA = 'TFRE'
	TRANSFERENCIA_ENVIADA = 'TFEN'

	TRANSACAO_CHOICES = [
        (DEPOSITO, 'Deposito'),
        (SAQUE, 'Saque'),
		(TRANSFERENCIA_RECEBIDA, 'Transferencia_Recebida'),
		(TRANSFERENCIA_ENVIADA, 'Transferencia_Enviada')
    ]

	id = models.AutoField(primary_key=True)
	data_hora = models.DateTimeField()
	valor = models.DecimalField(max_digits=15, decimal_places=2, default=0)
	tipo = models.CharField(max_length=5, choices=TRANSACAO_CHOICES)
	conta = models.ForeignKey(Conta, on_delete=models.CASCADE)

	def __str__(self) -> str:
		return self.id