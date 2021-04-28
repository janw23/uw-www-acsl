# Generated by Django 3.2 on 2021-04-28 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prover', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directory',
            name='opt_description',
            field=models.TextField(blank=True, verbose_name='optional description'),
        ),
        migrations.AlterField(
            model_name='file',
            name='opt_description',
            field=models.TextField(blank=True, verbose_name='optional description'),
        ),
        migrations.AlterField(
            model_name='filesection',
            name='opt_description',
            field=models.TextField(blank=True, verbose_name='optional description'),
        ),
        migrations.AlterField(
            model_name='filesection',
            name='opt_name',
            field=models.CharField(blank=True, max_length=256, verbose_name='optional name'),
        ),
    ]