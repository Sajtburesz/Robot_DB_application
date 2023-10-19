# Generated by Django 4.2.1 on 2023-10-19 13:39

import django.contrib.postgres.indexes
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attributes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(blank=True, choices=[('Pass', 'Pass'), ('Fail', 'Fail')], max_length=10, null=True)),
                ('log_message', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(blank=True, choices=[('Pass', 'Pass'), ('Fail', 'Fail')], max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestRun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attributes', models.JSONField(blank=True, null=True)),
                ('version', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='TestSuite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('test_run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='robot_test_management.testrun')),
            ],
        ),
        migrations.AddIndex(
            model_name='testrun',
            index=django.contrib.postgres.indexes.GinIndex(fields=['attributes'], name='robot_test__attribu_13d2b4_gin'),
        ),
        migrations.AddField(
            model_name='testcase',
            name='suite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='robot_test_management.testsuite'),
        ),
        migrations.AddField(
            model_name='keyword',
            name='test_case',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='robot_test_management.testcase'),
        ),
    ]
