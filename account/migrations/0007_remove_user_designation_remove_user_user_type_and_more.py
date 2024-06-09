# Generated by Django 4.2.5 on 2023-10-23 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_role_userrole_name'),
        ('account', '0006_remove_user_occupation_remove_user_weight_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='designation',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_type',
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.userrole'),
        ),
    ]
