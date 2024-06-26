# Generated by Django 4.2.1 on 2023-10-21 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('robot_test_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='test_case',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='keywords', to='robot_test_management.testcase'),
        ),
        migrations.AlterField(
            model_name='testcase',
            name='suite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_cases', to='robot_test_management.testsuite'),
        ),
        migrations.AlterField(
            model_name='testsuite',
            name='test_run',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suites', to='robot_test_management.testrun'),
        ),
    ]
