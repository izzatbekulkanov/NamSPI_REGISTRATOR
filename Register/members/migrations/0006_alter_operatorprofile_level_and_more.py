# Generated by Django 5.2 on 2025-04-16 15:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_dailyworkwindow_is_leader'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operatorprofile',
            name='level',
            field=models.CharField(choices=[('Boshlovchi', '🟢 Boshlovchi'), ('Oddiy', '⭐ Oddiy'), ('Yaxshi', '🌟 Yaxshi'), ('Usta', '🔥 Usta'), ('VIP', '👑 VIP')], default='Boshlovchi', max_length=20),
        ),
        migrations.AlterField(
            model_name='operatorprofile',
            name='operator',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
