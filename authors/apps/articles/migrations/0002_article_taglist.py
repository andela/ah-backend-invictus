# Generated by Django 2.1 on 2019-05-05 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_tags', '0001_initial'),
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='tagList',
            field=models.ManyToManyField(related_name='articles', to='article_tags.ArticleTag'),
        ),
    ]
