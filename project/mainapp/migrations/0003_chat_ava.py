# Generated by Django 4.1.7 on 2023-03-31 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_chat_group_message_remove_target_author_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='ava',
            field=models.ImageField(null=True, upload_to='avatars/'),
        ),
    ]
