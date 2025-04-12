# Generated by Django 5.1.6 on 2025-04-12 09:30

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dropout', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Intervention',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('intervention_type', models.CharField(choices=[('counseling', 'Counseling Program'), ('financial', 'Financial Support'), ('academic', 'Academic Support'), ('community', 'Community Outreach'), ('infrastructure', 'Infrastructure Improvement'), ('other', 'Other')], max_length=20)),
                ('school_name', models.CharField(blank=True, max_length=255, null=True)),
                ('area', models.CharField(blank=True, max_length=100, null=True)),
                ('target_gender', models.CharField(blank=True, max_length=1, null=True)),
                ('target_caste', models.CharField(blank=True, max_length=100, null=True)),
                ('target_standard', models.CharField(blank=True, max_length=10, null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('planned', 'Planned'), ('ongoing', 'Ongoing'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='planned', max_length=10)),
                ('budget', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='studentdropout',
            name='dropout_year',
        ),
        migrations.AddField(
            model_name='studentdropout',
            name='date_of_dropout',
            field=models.DateField(default='2023-01-01'),
        ),
        migrations.AddField(
            model_name='studentdropout',
            name='reason',
            field=models.TextField(default='Unknown'),
        ),
        migrations.AlterField(
            model_name='studentdropout',
            name='age',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='studentdropout',
            name='gender',
            field=models.CharField(max_length=10),
        ),
    ]
