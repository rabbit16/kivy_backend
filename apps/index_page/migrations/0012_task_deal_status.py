# Generated by Django 5.1.2 on 2024-12-27 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index_page', '0011_task_pic_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='deal_status',
            field=models.BooleanField(db_index=True, default=False, verbose_name='任务状态'),
        ),
    ]
