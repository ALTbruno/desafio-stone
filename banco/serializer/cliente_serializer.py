import re
import datetime
from rest_framework import serializers

from banco.model.cliente import Cliente

class ClienteSerializer(serializers.ModelSerializer):

	cpf = serializers.CharField(min_length=11)
	
	class Meta():
		model = Cliente
		fields = [
			'id',
			'nome',
			'sobrenome',
			'data_nascimento',
			'cpf',
			'email',
			'senha'
		]

	def validate_cpf(self, cpf):
		if not re.match(r'^([\s\d]+)$', cpf):
			raise serializers.ValidationError(
			'O campo CPF deve ser numérico'
			)
		if len(cpf) < 11 or len(cpf) > 11:
			raise serializers.ValidationError(
			'O campo CPF deve ter 11 caracteres'
			)
		return cpf

	def validate_email(self, email):
		if not re.match(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email):
			raise serializers.ValidationError(
				'E-mail inválido'
			)
		return email

	def validate_data_nascimento(self, data_nascimento):
		hoje = datetime.datetime.today()
		idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
		if idade < 18:
			raise serializers.ValidationError(
				'Apenas pessoas com 18 ou mais anos podem abrir conta'
			)
		if data_nascimento.__gt__(hoje):
			raise serializers.ValidationError(
				'A data de nascimento não pode ser no futuro'
			)
		return data_nascimento
	
	def validate_senha(self, senha):
		if len(senha) < 8:
			raise serializers.ValidationError(
				 'A senha deve ter no mínimo 8 caracteres'
			)
