# Generated by Django 3.0.8 on 2021-07-23 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizApp', '0016_remove_quiz_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='time_finished',
            field=models.DateTimeField(),
        ),
    ]
