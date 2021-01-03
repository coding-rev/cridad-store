# Generated by Django 3.1.3 on 2021-01-02 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20210101_1255'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='photo_four',
            field=models.ImageField(default='mobile-slide.jpg', upload_to='gallery/items'),
        ),
        migrations.AddField(
            model_name='item',
            name='photo_three',
            field=models.ImageField(default='mobile-slide.jpg', upload_to='gallery/items'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.CharField(choices=[('False', 'False'), ('True', 'True'), ('New', 'New')], default='New', max_length=10),
        ),
    ]
