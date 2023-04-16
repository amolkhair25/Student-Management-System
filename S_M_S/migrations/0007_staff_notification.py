# Generated by Django 3.1.3 on 2023-04-05 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('S_M_S', '0006_auto_20230403_2223'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff_Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='S_M_S.staff')),
            ],
        ),
    ]
