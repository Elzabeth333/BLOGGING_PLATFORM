# Generated by Django 5.0.6 on 2024-07-04 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpanel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='status',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.CharField(max_length=50),
        ),
    ]
