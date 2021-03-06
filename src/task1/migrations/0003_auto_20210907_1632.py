# Generated by Django 3.2.7 on 2021-09-07 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task1', '0002_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='idempotency_key',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.EmailField(max_length=50, unique=True),
        ),
        migrations.AddIndex(
            model_name='account',
            index=models.Index(fields=['email'], name='task1_accou_email_d70060_idx'),
        ),
        migrations.AddIndex(
            model_name='transaction',
            index=models.Index(fields=['idempotency_key'], name='task1_trans_idempot_381e1d_idx'),
        ),
    ]
