# Generated by Django 3.0.4 on 2020-03-17 11:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0005_csvfiledata'),
    ]

    operations = [
        migrations.RenameField(
            model_name='csvfiledata',
            old_name='Academic',
            new_name='Academic_Review',
        ),
        migrations.RenameField(
            model_name='csvfiledata',
            old_name='Behavior',
            new_name='Behavior_Review',
        ),
        migrations.RemoveField(
            model_name='csvfiledata',
            name='Review',
        ),
    ]