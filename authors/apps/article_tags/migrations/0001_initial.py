# Generated by Django 2.1 on 2019-05-03 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_tag_text', models.CharField(max_length=70, unique=True)),
            ],
        ),
    ]
