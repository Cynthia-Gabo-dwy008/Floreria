# Generated by Django 2.2.6 on 2019-10-23 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Flores',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('valor', models.IntegerField()),
                ('descripcion', models.TextField()),
                ('stock', models.IntegerField()),
                ('fotografia', models.ImageField(null=True, upload_to='flores')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='floreria.Estado')),
            ],
        ),
    ]