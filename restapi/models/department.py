from django.db import models
from .clinic import Clinic


class Department(models.Model):

    DEPARTMENT_TYPES = (
        ('lab', 'Lab'),
        ('clinical', 'Clinical'),
        ('environment', 'Environment'),
    )

    name = models.CharField(max_length=200)
    type = models.CharField(max_length=50, choices=DEPARTMENT_TYPES)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name