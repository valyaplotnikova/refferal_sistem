import random
import string

from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """ Модель пользователя. """

    username = None
    phone_number = models.CharField(max_length=20, unique=True)
    invitation_code = models.CharField(max_length=6, unique=True, **NULLABLE)
    activated_invitation_code = models.CharField(max_length=6, **NULLABLE)
    inviter = models.ForeignKey('self', related_name='invitings', on_delete=models.SET_NULL, **NULLABLE)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def generate_invitation_code(self):
        self.invitation_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.save()

    def __str__(self):
        return self.phone_number

    def save(self, *args, **kwargs):
        if not self.invitation_code:
            self.generate_invitation_code()  # Generate code on first save
        super().save(*args, **kwargs)

    def clean(self) -> None:
        if self.inviter == self:
            raise ValidationError(
                {"inviter": "Приглашение самого себя запрещено"},
            )
        return super().clean()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('phone_number',)
