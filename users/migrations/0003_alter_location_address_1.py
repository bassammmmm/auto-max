# Generated by Django 4.1.7 on 2023-03-02 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='address_1',
            field=models.CharField(default='', max_length=100, null=True),
        ),
    ]
