# Generated by Django 4.2.6 on 2023-10-24 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('resource_id', models.AutoField(primary_key=True, serialize=False)),
                ('resource_name', models.CharField(blank=True, max_length=100, null=True)),
                ('resource_url', models.URLField(blank=True)),
                ('top_tag', models.CharField(blank=True, max_length=100, null=True)),
                ('bottom_tag', models.CharField(blank=True, max_length=100, null=True)),
                ('title_cut', models.CharField(blank=True, max_length=100, null=True)),
                ('date_cut', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('link', models.URLField(blank=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('nd_date', models.DateTimeField()),
                ('s_date', models.DateTimeField(auto_now_add=True)),
                ('not_date', models.DateField()),
                ('res_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parsersystem.resource')),
            ],
        ),
    ]