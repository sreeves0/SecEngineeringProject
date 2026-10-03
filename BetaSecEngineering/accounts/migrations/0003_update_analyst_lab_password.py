from django.db import migrations


def update_analyst_password(apps, schema_editor):
    lab_account = apps.get_model('accounts', 'LabAccount')
    lab_account.objects.filter(username='analyst').update(
        lab_password='secengy124!'
    )


def restore_analyst_password(apps, schema_editor):
    lab_account = apps.get_model('accounts', 'LabAccount')
    lab_account.objects.filter(username='analyst').update(
        lab_password='demo-pass-1'
    )


class Migration(migrations.Migration):
    dependencies = [('accounts', '0002_seed_lab_accounts')]

    operations = [
        migrations.RunPython(update_analyst_password, restore_analyst_password),
    ]
