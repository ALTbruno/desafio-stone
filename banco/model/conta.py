from tkinter import CASCADE
from django.db import models

from banco.model.cliente import Cliente

class Conta(models.Model):
	id = models.AutoField(primary_key=True)
	agencia = models.CharField(max_length=4)
	numero = models.CharField(max_length=10)
	saldo = models.DecimalField(max_digits=15, decimal_places=2, default=0)
	cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)

	def __str__(self) -> str:
		return self.numero
