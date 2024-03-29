# Generated by Django 4.2.7 on 2023-12-20 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0005_portfolio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='bought_for',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='date_acquired',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='notes',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
