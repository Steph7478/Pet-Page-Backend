# Generated by Django 5.2.3 on 2025-07-25 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='status',
            field=models.CharField(choices=[('pendente', 'pendente'), ('disponivel', 'disponivel'), ('adotado', 'adotado')], default='disponivel', max_length=100),
        ),
    ]
