from django.contrib.auth.models import AbstractUser
import uuid
from django.db import models
from django.core.validators import MinValueValidator



class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18)]
    )

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "age"]



