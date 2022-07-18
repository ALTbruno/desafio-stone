import re
import datetime
from rest_framework import serializers

from banco.model.cliente import Cliente

class ClienteSerializer(serializers.ModelSerializer):

	cpf = serializers.CharField(min_length=11)
	
	class Meta():
		model = Cliente
		fields = "__all__"

	def validate_cpf(self, cpf):
		if not re.match(r'^([\s\d]+)$', cpf):
			raise serializers.ValidationError(
				{'CPF': 'CPF deve ser numérico'}
			)
		return cpf

	def validate_email(self, email):
		if not re.match(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email):
			raise serializers.ValidationError(
				{'email': 'E-mail inválido'}
			)
		return email

	def validate_data_nascimento(self, data_nascimento):
		if data_nascimento.__gt__(datetime.datetime.today()):
			raise serializers.ValidationError(
				{'data_nascimento': 'A data de nascimento não pode ser no futuro'}
			)
		return data_nascimento