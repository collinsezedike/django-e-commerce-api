# Generated by Django 4.2.1 on 2023-07-23 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_token_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Token',
        ),
    ]