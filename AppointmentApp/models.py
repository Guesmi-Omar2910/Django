from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class Status(models.TextChoices):
    PENDING = 'Pending', 'En attente'
    CONFIRMED = 'Confirmed', 'Confirmé'
    CANCELLED = 'Cancelled', 'Annulé'


class Appointment(models.Model):
    """Rendez-vous médical — entité associative reliant un médecin et un patient."""

    doctor = models.ForeignKey(
        'AccountApp.Doctor',
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name="Médecin"
    )
    patient = models.ForeignKey(
        'AccountApp.Patient',
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name="Patient"
    )
    reason = models.TextField(verbose_name="Motif de consultation")
    prescription = models.FileField(
        upload_to='prescriptions/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        verbose_name="Ordonnance (PDF)"
    )
    duration_minutes = models.PositiveIntegerField(
        default=30,
        verbose_name="Durée (minutes)"
    )
    appointment_date = models.DateTimeField(verbose_name="Date du rendez-vous")
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Statut"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")

    def clean(self):
        """
        Valide que appointment_date est dans le futur uniquement à la création
        ou lorsque la date est modifiée. Un RDV passé reste modifiable
        (ex. pour ajouter l'ordonnance).
        """
        if self.appointment_date:
            # À la création (pk est None) OU si la date a changé
            if self.pk is None:
                if self.appointment_date <= timezone.now():
                    raise ValidationError({
                        'appointment_date': "La date du rendez-vous doit être postérieure à maintenant."
                    })
            else:
                # Mise à jour : vérifier si appointment_date a changé
                try:
                    original = Appointment.objects.get(pk=self.pk)
                    if original.appointment_date != self.appointment_date:
                        if self.appointment_date <= timezone.now():
                            raise ValidationError({
                                'appointment_date': "La date du rendez-vous doit être postérieure à maintenant."
                            })
                except Appointment.DoesNotExist:
                    pass

    def __str__(self):
        return f"RDV {self.doctor} — {self.patient} le {self.appointment_date.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = "Rendez-vous"
        verbose_name_plural = "Rendez-vous"
        ordering = ['appointment_date']
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date'],
                name='unique_doctor_appointment_date'
            )
        ]