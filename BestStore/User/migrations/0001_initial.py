# Generated by Django 2.2.1 on 2019-05-29 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, null=True)),
                ('email', models.EmailField(max_length=50, null=True)),
                ('subject', models.CharField(max_length=30, null=True)),
                ('query', models.TextField()),
            ],
        ),
    ]
