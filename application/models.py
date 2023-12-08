from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _


class Human_Gender(models.Model):
    gender_id = models.AutoField(primary_key=True)
    gender_name = models.CharField(max_length=9)
    
    class Meta:
        verbose_name = _('gender')
        verbose_name_plural = _('genders')
    def __str__(self):
        return self.gender_name

class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(
        name='username',
        max_length=128,
        unique=True,
        help_text=_('Required. 128 characters or fewer. Letters, digits and @/./-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
        verbose_name=_('Username')
    )
    user_gender = models.ForeignKey(
        to='Human_Gender', 
        default=None, 
        null=True,
        on_delete=models.RESTRICT,
        verbose_name=_('Human Gender')
    )
    user_first_name = models.CharField(
        max_length=64, blank=False,
        verbose_name=_('First name')
    )
    user_last_name = models.CharField(
        max_length=64, blank=False,
        verbose_name=_('Last name')
    )
    user_patronymic = models.CharField(
        max_length=64, blank=True, null=True,
        verbose_name=_('Patronymic')
    )
    user_email = models.EmailField(
        max_length=256, blank=True,
        verbose_name=_('E-mail')
    )
    phone_regex = RegexValidator(regex=r'^\+?\d{9,15}$', 
                                 message=_("Phone number must match the format: '+999999999'. Max 15 digits."))
    user_phone = models.CharField(
        validators=[phone_regex], max_length=16, blank=False,
        verbose_name=_('Phone number')
    )
    avatar = models.ImageField(
        upload_to='avatars/', null=True, blank=True,
        verbose_name=_('Avatar')
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('Is staff')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Is active')
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Joined')
    )

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "user_email"
    REQUIRED_FIELDS = ['user_first_name', 'user_last_name', 'user_patronymic','user_phone', 'user_email']

    objects = CustomUserManager()
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def get_full_name(self):
        full_name = '%s %s' % (self.user_last_name, self.user_first_name)
        if (self.user_patronymic) :
            full_name += ' '+self.user_patronymic
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
    
    @classmethod
    def get_email_field_name(cls):
        try:
            return cls.EMAIL_FIELD
        except AttributeError:
            return "user_email"
    def get_full_info(self):
        temp_patr = '' if self.user_patronymic is None else self.user_patronymic
        return "Id=" + str(self.user_id) + ";\n" + \
            _("username=") + self.username + ";\n" + \
            _("first name=") + self.user_first_name + ";\n" + \
            _("last name=") + self.user_last_name + ";\n" + \
            _("patronymic=") + temp_patr + ";\n" + \
            _("phone=") + self.user_phone + ";\n" + \
            _("email=") + self.user_email + "."
    
    def __str__(self):
        temp_patr = '' if self.user_patronymic is None else self.user_patronymic
        return_text = "Id=" + str(self.user_id) + ";\n" + \
            _("first name=") + self.user_first_name + ";\n" + \
            _("last name=") + self.user_last_name
        if (self.user_patronymic):
            return_text += _("patronymic=") + temp_patr
        return_text += "."
        return return_text

class Abonement_Type(models.Model):
    abonement_type_id = models.AutoField(
        primary_key=True,
        verbose_name='id'
    )
    abonement_type = models.CharField(
        max_length=64, blank=False,
        verbose_name=_('Abonement type')
    )
    class Meta:
        verbose_name = _('abonement type')
        verbose_name_plural = _('abonement types')
    def __str__(self):
        return self.abonement_type

class Abonement(models.Model):
    abonement_id = models.AutoField(
        primary_key=True,
        verbose_name='id'
    )
    abonement_type = models.ForeignKey(
        to='Abonement_Type', on_delete=models.RESTRICT, blank=False,
        verbose_name=_('Abonement type id')
    )
    opened = models.DateField(
        auto_now=False, auto_now_add=False, blank=False,
        verbose_name=_('Opened')
    )
    expires = models.DateField(
        auto_now=False, auto_now_add=False, blank=False,
        verbose_name=_('Expires')
    )
    class Meta:
        verbose_name = _('abonement')
        verbose_name_plural = _('abonements')
    def __str__(self):
        return "Id=" + self.abonement_id + \
        _("type=") + self.abonement_type + \
        _("opened=") + self.opened + \
        _("expires=") + self.expires + "."


class Training_Type(models.Model):
    training_type_id = models.AutoField(
        primary_key=True,
        verbose_name='id'
    )
    training_type = models.CharField(
        max_length=64, blank=False,
        verbose_name=_('Training type')
    )
    class Meta:
        verbose_name = _('training type')
        verbose_name_plural = _('training types')
    def __str__(self):
        return self.training_type

class Training(models.Model):
    training_id = models.AutoField(
        primary_key=True,
        verbose_name='id'
    )
    training_type = models.ForeignKey(
        to='Training_Type', 
        on_delete=models.RESTRICT, 
        blank=False,
        verbose_name=_('Training type')
    )
    training_date = models.DateField(
        auto_now=False, auto_now_add=False,
        verbose_name=_('Training date')
    )
    training_leader = models.ForeignKey(
        to='CustomUser',
        on_delete=models.CASCADE, 
        blank=False,
        verbose_name=_('Training leader')
    )
    class Meta:
        verbose_name = _('training')
        verbose_name_plural = _('trainings')
    def __str__(self):
        return f"{self.training_id}: {self.training_type}, {self.training_date}."
