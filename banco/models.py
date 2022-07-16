from tkinter import CASCADE
from django.db import models

# Create your models here.
class Cliente(models.Model):
	id = models.AutoField(primary_key=True)
	nome = models.CharField(max_length=50)
	sobrenome = models.CharField(max_length=150)
	dataNascimento = models.DateField
	cpf = models.CharField(max_length=11)
	email = models.CharField(max_length=255)

class Conta(models.Model):
	id = models.AutoField(primary_key=True)
	agencia = models.CharField(max_length=4)
	numero = models.CharField(max_length=10)
	saldo = models.DecimalField(max_digits=15, decimal_places=2, default=0)
	cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
