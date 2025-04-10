# Generated by Django 4.2.20 on 2025-04-09 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_post_file_post_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='posts', to='board.tag'),
        ),
    ]
