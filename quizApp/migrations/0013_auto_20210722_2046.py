# Generated by Django 3.0.8 on 2021-07-22 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizApp', '0012_auto_20210722_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='time_finished',
            field=models.DateTimeField(null=True),
        ),
    ]
