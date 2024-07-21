from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import CustomUserManager

# Create your models here.



class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'