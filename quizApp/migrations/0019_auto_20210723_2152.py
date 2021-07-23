# Generated by Django 3.0.8 on 2021-07-23 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizApp', '0018_participantanswer_connect_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParticipantAnswer_Question_Quiz_connections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participant_answer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quizApp.ParticipantAnswer')),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quizApp.Question')),
                ('quiz', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quizApp.Quiz')),
            ],
        ),
        migrations.DeleteModel(
            name='ParticipantAnswer_connect_Question',
        ),
    ]
