# Generated by Django 5.0.6 on 2024-07-09 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_delete_attendance'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classname',
            options={'verbose_name': 'Class', 'verbose_name_plural': 'Classes'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Profile', 'verbose_name_plural': 'Profiles'},
        ),
    ]
