from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if (not username):
            raise ValueError("Username must be set")
        if (not password):
            raise ValueError("Password must be set")
        #if (not gender):
        #    gender = Human_Gender.objects.get(gender_name = 'undefined')
        print (extra_fields)
        user = self.model(username=username,
                          **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(username=username, 
                                password=password,
                                **extra_fields)