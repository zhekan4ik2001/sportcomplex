from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordResetForm, _unicode_ci_compare
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from .models import CustomUser, Training, Training_Type

class CustomPassResetForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CustomPassResetForm, self).__init__(*args, **kwargs)
    
    user_email = forms.EmailField(required=True, label='user_email', 
                            label_suffix=None,
                            widget=forms.EmailInput(attrs={"autocomplete": "user_email"}),
                            help_text=_("Enter an email that associated with your account."))
    def clean_email(self):
        if (self.user_email.is_valid()):
            return self.cleaned_data.get('user_email')
        else:
            raise ValidationError(_('E-mail is incorrect! Check format.'))
    
    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")

        email_message.send()

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        email_field_name = CustomUser.get_email_field_name()
        print('!!! ' + email_field_name)
        
        active_users = CustomUser._default_manager.filter(
            **{
                "%s__iexact" % email_field_name: email,
                "is_active": True,
            }
        )
        return (
            u
            for u in active_users
            if u.has_usable_password()
            and _unicode_ci_compare(email, getattr(u, email_field_name))
        )

    def save(
        self,
        domain_override=None,
        subject_template_name="registration/password_reset_subject.txt",
        email_template_name="registration/password_reset_email.html",
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None,
    ):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        user_email = self.cleaned_data["user_email"]
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        email_field_name = CustomUser.get_email_field_name()
        for user in self.get_users(user_email):
            user_email = getattr(user, email_field_name)
            context = {
                "user_email": user_email,
                "domain": domain,
                "site_name": site_name,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                "token": token_generator.make_token(user),
                "protocol": "https" if use_https else "http",
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name,
                email_template_name,
                context,
                from_email,
                user_email,
                html_email_template_name=html_email_template_name,
            )


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'username', 'id': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '*****',
            'id': 'password',
        }
))

class TrainingSessionForm(forms.ModelForm):
    training_type = forms.ModelChoiceField(
        queryset=Training_Type.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'training_type',
            'required': 'True'
        }),
        label=_('Training type'))
    training_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'id': 'training_date',
            'required': 'True'
        }),
        label=_('Training date')
    )
    training_leader = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(groups__name='trainer'),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'training_type',
            'required': 'False'
        }),
        label=_('Training leader')
    )
    clients = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.filter(groups__name='client'),
        required=True,
        label=_('Clients'),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check',
            'id': 'training_type'
        }
        )
    )
    class Meta:
        model = Training
        fields = "__all__"
