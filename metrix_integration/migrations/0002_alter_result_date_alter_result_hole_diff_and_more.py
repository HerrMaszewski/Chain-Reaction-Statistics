# Generated by Django 5.0.1 on 2024-02-02 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metrix_integration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='hole_diff',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='hole_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='hole_ob',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='hole_result',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='total_competitions',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='total_difference_to_par',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='total_throws',
            field=models.IntegerField(default=0),
        ),
    ]
