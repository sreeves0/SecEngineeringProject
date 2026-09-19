from django.db import models


class LabAccount(models.Model):
    """Dummy credentials used only by the isolated SQL-injection lab."""

    username = models.CharField(max_length=80, unique=True)
    lab_password = models.CharField(max_length=120)
    display_name = models.CharField(max_length=120)

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username
