# Generated by Django 5.0.4 on 2024-04-28 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('slug', models.TextField(verbose_name='group/<django.db.models.fields.TextField>/')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='group',
            field=models.TextField(blank=True, null=True),
        ),
    ]
