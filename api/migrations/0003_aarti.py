# Generated by Django 4.2.3 on 2023-07-29 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_literature'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aarti',
            fields=[
                ('isActive', models.BooleanField(default=False)),
                ('groupId', models.CharField(default=1, max_length=40)),
                ('createdBy', models.CharField(default=1, max_length=50)),
                ('updatedBy', models.CharField(default=1, max_length=50)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('updatedDate', models.DateTimeField(auto_now=True)),
                ('aartiId', models.AutoField(primary_key=True, serialize=False)),
                ('aartiName', models.CharField(max_length=200)),
                ('aartiText', models.TextField()),
                ('isVerified', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]