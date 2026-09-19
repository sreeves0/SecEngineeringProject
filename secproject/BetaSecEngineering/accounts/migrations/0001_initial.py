from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='LabAccount',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('username', models.CharField(max_length=80, unique=True)),
                ('lab_password', models.CharField(max_length=120)),
                ('display_name', models.CharField(max_length=120)),
            ],
            options={'ordering': ['username']},
        ),
    ]
