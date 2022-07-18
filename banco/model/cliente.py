from tkinter import CASCADE
from django.db import models

# Create your models here.
class Cliente(models.Model):
	id = models.AutoField(primary_key=True)
	nome = models.CharField(max_length=50, null=True)
	sobrenome = models.CharField(max_length=150, null=True)
	data_nascimento = models.DateField(null=True)
	cpf = models.CharField(max_length=11, null=True)
	email = models.CharField(max_length=255, null=True)
	senha = models.CharField(max_length=255, null=True)

	def __str__(self) -> str:
		return self.nome
