# Generated by Django 3.1.3 on 2023-04-14 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('S_M_S', '0013_student_feedback_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff_feedback',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
