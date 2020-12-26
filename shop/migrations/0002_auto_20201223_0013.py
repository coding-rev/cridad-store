# Generated by Django 3.1.3 on 2020-12-23 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='delivery_and_returns',
            field=models.TextField(default='We will deliver according to your location.'),
        ),
        migrations.AlterField(
            model_name='category',
            name='category',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.CharField(choices=[('True', 'True'), ('False', 'False'), ('New', 'New')], default='New', max_length=10),
        ),
    ]