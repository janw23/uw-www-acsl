# Generated by Django 3.2 on 2021-04-29 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prover', '0006_auto_20210429_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directory',
            name='available',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='file',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]