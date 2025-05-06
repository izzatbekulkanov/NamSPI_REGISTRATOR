from django.db import models
from members.models import CustomUser

class Section(models.Model):
    name = models.CharField(max_length=255, unique=True)  # masalan: Ilmiy faoliyat
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class SubService(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=255)  # masalan: Grantlar haqida maʼlumot
    description = models.TextField(blank=True, null=True)
    online_available = models.BooleanField(default=False)  # onlayn mavjudmi

    def __str__(self):
        return f"{self.name} ({self.section.name})"


class AssignedService(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service = models.ForeignKey(SubService, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'service')

    def __str__(self):
        return f"{self.user.full_name} - {self.service.name}"
