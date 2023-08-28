# Generated by Django 4.2.3 on 2023-08-01 04:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_aarti'),
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('isActive', models.BooleanField(default=False)),
                ('groupId', models.CharField(default=1, max_length=40)),
                ('createdBy', models.CharField(default=1, max_length=50)),
                ('updatedBy', models.CharField(default=1, max_length=50)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('updatedDate', models.DateTimeField(auto_now=True)),
                ('businessId', models.AutoField(primary_key=True, serialize=False)),
                ('businessName', models.CharField(max_length=200)),
                ('businessType', models.CharField(max_length=120)),
                ('businessNumber', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('website', models.CharField(max_length=220)),
                ('businessDescription', models.TextField()),
                ('isVerified', models.BooleanField(default=False)),
                ('cityId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='GetAllBusinessByCityId', to='api.city')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]