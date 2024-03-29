# Generated by Django 4.2.11 on 2024-03-19 11:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content',
            name='original_file',
        ),
        migrations.AddField(
            model_name='content',
            name='original_audio',
            field=models.FileField(blank=True, null=True, upload_to='contents/audio/%Y/%m/%d', verbose_name='Исходное аудио'),
        ),
        migrations.AddField(
            model_name='content',
            name='original_video',
            field=models.FileField(default=1, upload_to='contents/video/%Y/%m/%d', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('mp4',))], verbose_name='Исходное видео'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='content',
            name='output_audio',
            field=models.FileField(blank=True, null=True, upload_to='contents/output/audio/%Y/%m/%d', verbose_name='Окончательное аудио'),
        ),
        migrations.AddField(
            model_name='content',
            name='output_video',
            field=models.FileField(blank=True, null=True, upload_to='contents/output/video/%Y/%m/%d', verbose_name='Окончательное видео'),
        ),
    ]
