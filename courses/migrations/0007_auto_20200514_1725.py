# Generated by Django 3.0.6 on 2020-05-14 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20200514_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='courses/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='course',
            name='overview',
            field=models.TextField(),
        ),
    ]
