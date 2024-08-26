from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from core.models import Barber, Service

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.service.name} with {self.barber.user.get_full_name()}"
