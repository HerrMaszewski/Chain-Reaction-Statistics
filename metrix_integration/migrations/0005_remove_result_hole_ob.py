# Generated by Django 5.0.1 on 2024-02-02 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metrix_integration', '0004_alter_course_course_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='hole_ob',
        ),
    ]
