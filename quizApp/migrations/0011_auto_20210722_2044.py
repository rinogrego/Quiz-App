# Generated by Django 3.0.8 on 2021-07-22 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizApp', '0010_auto_20210722_0837'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='deadline',
            field=models.DateTimeField(default=None),
        ),
        migrations.AlterField(
            model_name='participant',
            name='time_finished',
            field=models.DateTimeField(default=None),
        ),
    ]
