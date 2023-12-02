from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail



class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, gender=None, **extra_fields):
        if (not username):
            raise ValueError("Username must be set")
        if (not password):
            raise ValueError("Password must be set")
        if (not gender):
            gender = Human_Gender.objects.get(gender_name = 'undefined')
        print (extra_fields, gender)
        user = self.model(username=username,
                          user_gender=gender,
                          **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, gender=None, patronymic=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(username=username, 
                                password=password, 
                                gender=gender,
                                **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(
        name='username',
        max_length=128,
        unique=True,
        help_text='Required. 128 characters or fewer. Letters, digits and @/./-/_ only.',
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    user_gender = models.ForeignKey(to='Human_Gender', on_delete=models.RESTRICT)
    user_first_name = models.CharField(max_length=64, blank=False)
    user_last_name = models.CharField(max_length=64, blank=False)
    user_patronymic = models.CharField(max_length=64, blank=True, null=True)
    user_email = models.EmailField(max_length=256, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?\d{9,15}$', 
                                 message="Номер телефона вводится в соответствии с форматом: '+999999999'. Максимум 15 цифр.")
    user_phone = models.CharField(validators=[phone_regex], max_length=16, blank=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ['user_first_name', 'user_last_name', 'user_patronymic','user_phone', 'user_email']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
    
    def get_full_name(self):
        full_name = '%s %s %s' % (self.user_last_name, self.user_first_name, self.user_patronymic)
        return full_name.strip()

    def get_short_name(self):
        return self.user_first_name

    def get_date_joined(self):
        return self.date_joined

    def get_date_joined(self):
        return self.date_joined
    
    def email_user(self, subject, message, from_email=None, **kwargs):
        # Sends an email to this User.
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return f"client id={self.user_id}; \n" \
            f"login={self.username} \n" \
            f"password hash={self.password} \n" \
            f"gender={self.user_gender} \n" \
            f"first name={self.user_first_name} \n" \
            f"second name={self.user_last_name} \n" \
            f"patronymic={self.user_patronymic} \n" \
            f"phone={self.user_phone} \n" \
            f"email={self.user_email}."

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
    gender_name = models.CharField(max_length=9)
    def __str__(self):
        return self.gender_name

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
