# Generated by Django 3.2.12 on 2022-02-13 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appImageA4', '0002_alter_userimage_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userimage',
            name='user_id',
        ),
    ]
