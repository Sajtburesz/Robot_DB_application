# Generated by Django 4.2.1 on 2023-10-21 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robot_test_management', '0002_alter_keyword_test_case_alter_testcase_suite_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='keyword',
            name='doc',
            field=models.TextField(blank=True, null=True),
        ),
    ]
