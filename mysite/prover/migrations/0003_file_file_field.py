# Generated by Django 3.2 on 2021-04-29 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prover', '0002_auto_20210428_2333'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='file_field',
            field=models.FileField(blank=True, upload_to='uploads/'),
        ),
    ]
