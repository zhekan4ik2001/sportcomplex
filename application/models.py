from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

class Abonement_Type(models.Model):
    abonement_type_id = models.AutoField(primary_key=True)
    abonement_type = models.CharField(max_length=64, blank=False)
    def __str__(self):
        return self.abonement_type

class Abonement(models.Model):
    abonement_id = models.AutoField(primary_key=True)
    abonement_type_id = models.ForeignKey('Abonement_Type', on_delete=models.RESTRICT, blank=False)
    opened = models.DateField(auto_now=False, auto_now_add=False, blank=False)
    expires = models.DateField(auto_now=False, auto_now_add=False, blank=False)
    def __str__(self):
        return f"id={self.abonement_id}, type={self.abonement_type_id}, opened={self.opened}, expires={self.expires}"

class Human_Gender(models.Model):
    gender_id = models.AutoField(primary_key=True)
    gender_name = models.CharField(max_length=6)
    def __str__(self):
        return self.gender_name

class Club_Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    client_gender = models.ForeignKey('Human_Gender', on_delete=models.RESTRICT)
    client_first_name = models.CharField(max_length=128, blank=False)
    client_second_name = models.CharField(max_length=128, blank=False)
    client_patronymic = models.CharField(max_length=128, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?\d{9,15}$', 
                                 message="Номер телефона вводится в соответствии с форматом: '+999999999'. Максимум 15 цифр.")
    client_phone = models.CharField(validators=[phone_regex], max_length=16, blank=False)
    client_email = models.EmailField(max_length=256, blank=True)
    def __str__(self):
        return f"client id={self.client_id}; \n" \
               f"login={self.client_passwd_hash} \n" \
               f"password hash={self.client_gender} \n" \
               f"first name={self.client_first_name} \n" \
               f"second name={self.client_second_name} \n" \
               f"patronymic={self.client_patronymic} \n" \
               f"phone={self.client_phone} \n" \
               f"email={self.client_email}."

class Training_Type(models.Model):
    training_type_id = models.AutoField(primary_key=True)
    training_type = models.CharField(max_length=64, blank=False)
    def __str__(self):
        return self.training_type

class Training(models.Model):
    training_id = models.AutoField(primary_key=True)
    training_type = models.ForeignKey('Training_Type', on_delete=models.RESTRICT, blank=False)
    training_date = models.DateField(auto_now=False, auto_now_add=False)
    def __str__(self):
        return f"{self.training_id}: {self.training_type}, {self.training_date}."

class Club_Trainer(models.Model):
    trainer_id = models.AutoField(primary_key=True)
    trainer_gender = models.ForeignKey('Human_Gender', on_delete=models.RESTRICT)
    trainer_first_name = models.CharField(max_length=128, blank=False)
    trainer_second_name = models.CharField(max_length=128, blank=False)
    trainer_patronymic = models.CharField(max_length=128, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?\d{9,15}$', 
                                 message="Номер телефона вводится в соответствии с форматом: '+999999999'. Максимум 15 цифр.")
    trainer_phone = models.CharField(validators=[phone_regex], max_length=16, blank=False)
    trainer_email = models.EmailField(max_length=256, blank=True)
    def __str__(self):
        return f"trainer id={self.client_id}; \n" \
               f"login={self.client_passwd_hash} \n" \
               f"password hash={self.client_gender} \n" \
               f"first name={self.client_first_name} \n" \
               f"second name={self.client_second_name} \n" \
               f"patronymic={self.client_patronymic} \n" \
               f"phone={self.client_phone} \n" \
               f"email={self.client_email}."
