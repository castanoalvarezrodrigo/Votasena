from django.contrib.auth.models import User
from django.db import IntegrityError, models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ficha = models.CharField(max_length=12, blank=True, help_text='Ficha del grupo de aprendices')

    def __str__(self):
        return f'{self.user.username} ({self.ficha})'

    class Meta:
        verbose_name = 'Aprendiz'
        verbose_name_plural = 'Aprendices'


class Candidacy(models.Model):
    ROLE_REPRESENTANTE = 'REP'
    ROLE_VOCERO = 'VOC'
    ROLE_SUBVOCERO = 'SUB'

    ROLE_CHOICES = [
        (ROLE_REPRESENTANTE, 'Representante'),
        (ROLE_VOCERO, 'Vocero'),
        (ROLE_SUBVOCERO, 'Subvocero'),
    ]

    name = models.CharField(max_length=120)
    role = models.CharField(max_length=3, choices=ROLE_CHOICES)
    ficha = models.CharField(max_length=12, blank=True, null=True, help_text='Ficha solo para vocero y subvocero')
    description = models.TextField(blank=True, verbose_name='Biografía', help_text='Una breve descripción personal del candidato')
    proposals = models.TextField(blank=True, help_text='Propuestas separadas por saltos de línea')
    profile_image = models.FileField(upload_to='candidates/', blank=True, null=True, help_text='Foto de perfil del candidato')

    def __str__(self):
        return f'{self.name} - {self.get_role_display()}'

    class Meta:
        verbose_name = 'Candidato'
        verbose_name_plural = 'Candidatos'
        ordering = ['role', 'name']


class Vote(models.Model):
    voter = models.ForeignKey(Profile, on_delete=models.CASCADE)
    candidacy = models.ForeignKey(Candidacy, on_delete=models.CASCADE)
    role = models.CharField(max_length=3, choices=Candidacy.ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Voto'
        verbose_name_plural = 'Votos'
        unique_together = [('voter', 'role')]

    def save(self, *args, **kwargs):
        if self.role != self.candidacy.role:
            raise IntegrityError('El rol del voto debe coincidir con el rol de la candidatura.')
        super().save(*args, **kwargs)


class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def is_valid(self):
        return not self.used and timezone.now() - self.created_at <= timedelta(minutes=30)

    def __str__(self):
        return f'Reset code for {self.user.username} - {self.code}'


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
