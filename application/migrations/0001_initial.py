# Generated by Django 4.1 on 2023-11-19 19:52

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Abonement_Type',
            fields=[
                ('abonement_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('abonement_type', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Human_Gender',
            fields=[
                ('gender_id', models.AutoField(primary_key=True, serialize=False)),
                ('gender_name', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Training_Type',
            fields=[
                ('training_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('training_type', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('training_id', models.AutoField(primary_key=True, serialize=False)),
                ('training_date', models.DateField()),
                ('training_type', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='application.training_type')),
            ],
        ),
        migrations.CreateModel(
            name='Club_Trainer',
            fields=[
                ('trainer_id', models.AutoField(primary_key=True, serialize=False)),
                ('trainer_first_name', models.CharField(max_length=128)),
                ('trainer_second_name', models.CharField(max_length=128)),
                ('trainer_patronymic', models.CharField(blank=True, max_length=128)),
                ('trainer_phone', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(message="Номер телефона вводится в соответствии с форматом: '+999999999'. Максимум 15 цифр.", regex='^\\+?\\d{9,15}$')])),
                ('trainer_email', models.EmailField(blank=True, max_length=256)),
                ('trainer_gender', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='application.human_gender')),
            ],
        ),
        migrations.CreateModel(
            name='Club_Client',
            fields=[
                ('client_id', models.AutoField(primary_key=True, serialize=False)),
                ('client_login', models.CharField(max_length=64)),
                ('client_password', models.CharField(max_length=64)),
                ('client_first_name', models.CharField(max_length=128)),
                ('client_second_name', models.CharField(max_length=128)),
                ('client_patronymic', models.CharField(blank=True, max_length=128)),
                ('client_phone', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(message="Номер телефона вводится в соответствии с форматом: '+999999999'. Максимум 15 цифр.", regex='^\\+?\\d{9,15}$')])),
                ('client_email', models.EmailField(blank=True, max_length=256)),
                ('client_gender', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='application.human_gender')),
            ],
        ),
        migrations.CreateModel(
            name='Abonement',
            fields=[
                ('abonement_id', models.AutoField(primary_key=True, serialize=False)),
                ('opened', models.DateField()),
                ('expires', models.DateField()),
                ('abonement_type_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='application.abonement_type')),
            ],
        ),
    ]
