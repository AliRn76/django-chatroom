# Generated by Django 3.0.2 on 2020-02-09 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
        migrations.AddField(
            model_name='chat',
            name='unread',
            field=models.BooleanField(default=False),
        ),
    ]
