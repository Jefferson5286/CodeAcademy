from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class UserModel(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(null=True, blank=True, max_length=11)

    is_tutor = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return str(self.id)
