# Generated by Django 3.2.7 on 2021-09-08 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task1', '0003_auto_20210907_1632'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='user_id',
            new_name='user',
        ),
    ]