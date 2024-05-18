# Generated by Django 5.0.6 on 2024-05-18 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apps_post", "0001_initial"),
        ("apps_user", "0002_alter_user_created_alter_user_updated"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="posts_liked",
            field=models.ManyToManyField(related_name="liked_by", to="apps_post.post"),
        ),
    ]
