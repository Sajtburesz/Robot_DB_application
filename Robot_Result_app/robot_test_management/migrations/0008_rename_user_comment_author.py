# Generated by Django 4.2.1 on 2023-10-23 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robot_test_management', '0007_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user',
            new_name='author',
        ),
    ]
