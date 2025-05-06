from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=100, blank=True, null=True)
    first_name_native = models.CharField(max_length=100, blank=True, null=True)
    second_name = models.CharField(max_length=100, blank=True, null=True)
    third_name = models.CharField(max_length=100, blank=True, null=True)

    image = models.URLField(blank=True, null=True)
    year_of_enter = models.CharField(max_length=10, blank=True, null=True)
    employee_id_number = models.PositiveIntegerField(blank=True, null=True)

    gender = models.CharField(max_length=20, blank=True, null=True)

    department_name = models.CharField(max_length=255, blank=True, null=True)
    department_structure = models.CharField(max_length=100, blank=True, null=True)
    department_locality = models.CharField(max_length=100, blank=True, null=True)

    academic_degree = models.CharField(max_length=100, blank=True, null=True)
    academic_rank = models.CharField(max_length=100, blank=True, null=True)

    employment_form = models.CharField(max_length=100, blank=True, null=True)
    employment_staff = models.CharField(max_length=100, blank=True, null=True)
    staff_position = models.CharField(max_length=100, blank=True, null=True)
    employee_status = models.CharField(max_length=100, blank=True, null=True)
    employee_type = models.CharField(max_length=100, blank=True, null=True)

    specialty = models.CharField(max_length=255, blank=True, null=True)
    contract_number = models.CharField(max_length=100, blank=True, null=True)
    decree_number = models.CharField(max_length=100, blank=True, null=True)

    contract_date = models.DateField(blank=True, null=True)
    decree_date = models.BigIntegerField(blank=True, null=True)
    birth_date = models.BigIntegerField(blank=True, null=True)
    created_at = models.BigIntegerField(blank=True, null=True)
    update_at = models.BigIntegerField(blank=True, null=True)

    hash = models.CharField(max_length=255, blank=True, null=True)

    # 🔒 Role flags
    is_leader = models.BooleanField(default=False, verbose_name="Rahbar")
    is_operator = models.BooleanField(default=True, verbose_name="Operator")

    def __str__(self):
        return self.full_name or self.username

    # 🔍 Custom role checkers
    def is_supervisor(self):
        return self.is_superuser or self.is_staff

    def role_title(self):
        """Foydalanuvchining roli"""
        if self.is_supervisor():
            return "Admin (Nazoratchi)"
        elif self.is_leader:
            return "Rahbar"
        elif self.is_operator:
            return "Operator"
        return "Foydalanuvchi"

    def role_badge(self):
        """UI badge uchun klass"""
        if self.is_supervisor():
            return "bg-dark text-white"
        elif self.is_leader:
            return "bg-danger text-white"
        elif self.is_operator:
            return "bg-primary text-white"
        return "bg-secondary text-white"


class DailyWorkWindow(models.Model):
    operator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='work_windows')
    date = models.DateField(default=now)
    window_number = models.PositiveIntegerField(null=True, blank=True)  # 🔧 Ruxsat berildi
    is_leader = models.BooleanField(default=False)

    class Meta:
        unique_together = ['operator', 'date']
        verbose_name = "Kundalik Ish Oynasi"
        verbose_name_plural = "Kundalik Ish Oynalari"

    def __str__(self):
        return f"{self.operator.full_name} - {self.date} - Oyna {self.window_number or 'Rahbar'}"


class OperatorProfile(models.Model):
    LEVELS = [
        ("Boshlovchi", "🟢 Boshlovchi"),
        ("Oddiy", "⭐ Oddiy"),
        ("Yaxshi", "🌟 Yaxshi"),
        ("Usta", "🔥 Usta"),
        ("VIP", "👑 VIP"),
    ]

    operator = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    total_served = models.PositiveIntegerField(default=0)
    level = models.CharField(max_length=20, choices=LEVELS, default="Boshlovchi")

    def update_level(self):
        served = self.total_served
        if served >= 500:
            self.level = "VIP"
        elif served >= 300:
            self.level = "Usta"
        elif served >= 150:
            self.level = "Yaxshi"
        elif served >= 50:
            self.level = "Oddiy"
        else:
            self.level = "Boshlovchi"

    def add_served(self):
        self.total_served += 1
        self.update_level()
        self.save()

    def __str__(self):
        return f"{self.operator.full_name} ({self.level})"