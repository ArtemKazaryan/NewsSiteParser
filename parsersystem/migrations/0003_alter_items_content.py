# Generated by Django 4.2.6 on 2023-10-25 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parsersystem', '0002_alter_items_link_alter_items_nd_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='content',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]
