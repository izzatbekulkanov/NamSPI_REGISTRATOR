# Generated by Django 5.2 on 2025-04-16 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0007_alter_dailyworkwindow_window_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_leader',
            field=models.BooleanField(default=False, verbose_name='Rahbar'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_operator',
            field=models.BooleanField(default=True, verbose_name='Operator'),
        ),
    ]
