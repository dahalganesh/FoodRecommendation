# Generated by Django 3.1.2 on 2021-07-31 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recommapp', '0010_auto_20210731_1006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='user',
        ),
        migrations.AddField(
            model_name='review',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='recommapp.customer'),
        ),
    ]
