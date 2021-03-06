# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-21 11:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100)),
                ('created', models.DateField(auto_now_add=True)),
                ('users', models.ManyToManyField(related_name='group_users', to='users.User')),
                ('userss', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin_group', to='users.User')),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(null=True, upload_to='medias/')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255)),
                ('photo', models.FileField(null=True, upload_to='chatroom/')),
                ('chatgroup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatroom.ChatGroup')),
                ('users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User')),
            ],
        ),
        migrations.AddField(
            model_name='media',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatroom.Message'),
        ),
    ]
