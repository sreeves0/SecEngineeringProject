from django.db import migrations


def seed_lab_accounts(apps, schema_editor):
    lab_account = apps.get_model('accounts', 'LabAccount')
    lab_account.objects.get_or_create(
        username='analyst',
        defaults={
            'lab_password': 'demo-pass-1',
            'display_name': 'Demo Analyst',
        },
    )
    lab_account.objects.get_or_create(
        username='auditor',
        defaults={
            'lab_password': 'demo-pass-2',
            'display_name': 'Demo Auditor',
        },
    )


def remove_lab_accounts(apps, schema_editor):
    lab_account = apps.get_model('accounts', 'LabAccount')
    lab_account.objects.filter(username__in=['analyst', 'auditor']).delete()


class Migration(migrations.Migration):
    dependencies = [('accounts', '0001_initial')]

    operations = [migrations.RunPython(seed_lab_accounts, remove_lab_accounts)]
