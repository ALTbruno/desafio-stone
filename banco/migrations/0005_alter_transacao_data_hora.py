# Generated by Django 4.0.6 on 2022-07-17 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banco', '0004_transacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transacao',
            name='data_hora',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
