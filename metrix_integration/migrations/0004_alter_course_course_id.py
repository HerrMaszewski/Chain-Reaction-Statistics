# Generated by Django 5.0.1 on 2024-02-02 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metrix_integration', '0003_remove_course_par'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_id',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]
