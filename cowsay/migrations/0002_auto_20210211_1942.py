# Generated by Django 3.1.6 on 2021-02-11 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cowsay', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.CharField(max_length=100),
        ),
    ]