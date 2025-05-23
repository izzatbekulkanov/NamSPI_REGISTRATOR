# Generated by Django 5.2 on 2025-04-15 14:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('queueing', '0002_remove_service_category_alter_queueticket_service_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='queueticket',
            name='ended_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='queueticket',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='queueticket',
            name='result',
            field=models.CharField(blank=True, choices=[('completed', 'Bajarildi'), ('rejected', 'Rad etildi')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='queueticket',
            name='served_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='served_tickets', to=settings.AUTH_USER_MODEL, verbose_name='Operator'),
        ),
        migrations.AddField(
            model_name='queueticket',
            name='started_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
