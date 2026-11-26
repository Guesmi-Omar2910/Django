from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_past_date(value):
    """Valide que la date est antérieure à aujourd'hui."""
    if value >= timezone.localdate():
        raise ValidationError("La date de naissance doit être antérieure à la date du jour.")


class User(AbstractUser):
    """Modèle utilisateur personnalisé — point d'extension du projet."""
    pass


class Specialty(models.Model):
    """Spécialité médicale (Cardiologie, Dermatologie, Pédiatrie…)."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Spécialité"
        verbose_name_plural = "Spécialités"
        ordering = ['name']


class Doctor(User):
    """Médecin — hérite de User (héritage multi-tables)."""
    phone = models.CharField(
        max_length=8,
        validators=[RegexValidator(r'^\d{8}$', message="Le numéro de téléphone doit contenir exactement 8 chiffres.")]
    )
    license_number = models.CharField(
        max_length=6,
        unique=True,
        validators=[MinLengthValidator(6, message="Le numéro de licence doit contenir exactement 6 caractères.")]
    )
    specialties = models.ManyToManyField(
        Specialty,
        blank=True,
        related_name='doctors',
        verbose_name="Spécialités"
    )

    def __str__(self):
        return f"Dr. {self.last_name} {self.first_name}"

    class Meta:
        verbose_name = "Médecin"
        verbose_name_plural = "Médecins"


class Patient(User):
    """Patient — hérite de User (héritage multi-tables)."""
    phone = models.CharField(
        max_length=8,
        validators=[RegexValidator(r'^\d{8}$', message="Le numéro de téléphone doit contenir exactement 8 chiffres.")]
    )
    birth_date = models.DateField(
        validators=[validate_past_date]
    )
    national_id = models.CharField(
        max_length=8,
        unique=True,
        validators=[RegexValidator(r'^\d{8}$', message="Le numéro de CIN doit contenir exactement 8 chiffres.")]
    )

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
