from django.db import models
from registrator.models import SubService
from members.models import CustomUser


class QueueTicket(models.Model):
    STATUS_CHOICES = [
        ("waiting", "Kutmoqda"),
        ("serving", "Xizmat ko‘rsatilmoqda"),
        ("done", "Yakunlangan"),
    ]

    RESULT_CHOICES = [
        ("completed", "Bajarildi"),
        ("rejected", "Rad etildi"),
    ]

    service = models.ForeignKey(SubService, on_delete=models.CASCADE, related_name="tickets")
    ticket_number = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="waiting")
    window_number = models.PositiveIntegerField(null=True, blank=True, verbose_name="Oyna raqami")  # ✅ Yangi maydon
    # ✅ Qo‘shimcha maydonlar:
    served_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name="served_tickets", verbose_name="Operator")
    started_at = models.DateTimeField(null=True, blank=True)  # qabul bosilganda
    ended_at = models.DateTimeField(null=True, blank=True)  # bajarilganda yoki rad etilganda
    result = models.CharField(max_length=20, choices=RESULT_CHOICES, null=True, blank=True)  # natija

    notes = models.TextField(blank=True, null=True)  # ixtiyoriy izoh (agar kerak bo‘lsa)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.ticket_number} - {self.service.name}"

    def get_duration(self):
        """Xizmat davomiyligi (sekundlarda yoki datetime formatda)"""
        if self.started_at and self.ended_at:
            return (self.ended_at - self.started_at).total_seconds()
        return None
