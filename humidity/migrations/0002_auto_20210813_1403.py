# Generated by Django 3.2.4 on 2021-08-13 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('humidity', '0001_initial'),
    ]

    def insert_data(apps,schema_editior):
        Exhaust = apps.get_model('humidity', 'Exhaust')
        exhaust = Exhaust(pk=1,job_id='button_relay_job_id_17',status='False',automation_status='True')
        exhaust.save()
        exhaust = Exhaust(pk=2,job_id='button_relay_job_id_18',status='False',automation_status='True')
        exhaust.save()

    operations = [
        migrations.RunPython(insert_data)
    ]
