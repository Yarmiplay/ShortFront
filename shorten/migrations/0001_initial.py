# Generated by Django 5.0.1 on 2024-01-30 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Links',
            fields=[
                ('key', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('dest', models.URLField()),
                ('hit_count', models.IntegerField(default=0)),
            ],
        ),
    ]
