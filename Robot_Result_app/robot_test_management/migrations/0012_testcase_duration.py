# Generated by Django 4.2.6 on 2023-11-02 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robot_test_management', '0011_alter_testrun_options_alter_testrun_executed_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='testcase',
            name='duration',
            field=models.FloatField(blank=True, null=True),
        ),
    ]