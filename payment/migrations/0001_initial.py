# Generated by Django 4.0 on 2022-11-13 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=300)),
                ('last_name', models.CharField(max_length=300)),
                ('email', models.EmailField(max_length=254)),
                ('payment_approved', models.BooleanField(default=False)),
                ('mail_sent', models.BooleanField(default=False)),
            ],
        ),
    ]
