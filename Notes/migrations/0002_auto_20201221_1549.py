# Generated by Django 3.1.4 on 2020-12-21 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diary',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
