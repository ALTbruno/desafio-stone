# Generated by Django 4.0.6 on 2022-07-18 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banco', '0008_alter_cliente_nome_alter_cliente_sobrenome'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='cpf',
            field=models.CharField(max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='email',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='senha',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
