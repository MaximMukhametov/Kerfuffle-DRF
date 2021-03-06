# Generated by Django 3.0.7 on 2020-08-11 11:05
import json
import os
from django.db import migrations


def forward_func(apps, schema_editor):
    """Generate users data set, from json file"""
    User = apps.get_model("users", "User")
    script_dir = os.path.dirname(__file__)
    with open(script_dir + "/initial_users_data/new_db.json",'r') as initial_data:
        initial_data = json.load(initial_data)
        for user in initial_data:
            User.objects.create(name=user['name'],
                                status=user['status'])


# logic for migrating backwards
def reverse_func(apps, schema_editor):
    User = apps.get_model("eats", "Ingredient")
    User.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(forward_func, reverse_func)
    ]
