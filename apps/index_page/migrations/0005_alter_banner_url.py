# Generated by Django 5.1.2 on 2024-12-02 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index_page', '0004_alter_user_employee_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='url',
            field=models.CharField(max_length=10638, verbose_name='url地址'),
        ),
    ]
