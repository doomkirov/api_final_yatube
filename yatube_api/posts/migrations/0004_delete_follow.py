# Generated by Django 2.2.16 on 2022-08-16 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_post_group'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Follow',
        ),
    ]
