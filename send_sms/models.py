from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Carrier(models.Model):
    name = models.TextField(max_length=100)
    email_extension = models.TextField(max_length=100, verbose_name="Email extension (not including @)")

    def __str__(self):
        return self.name


class PhoneNumber(models.Model):
    user = models.OneToOneField(User)
    phone_number = models.IntegerField(max_length=10, null=True)
    carrier = models.ForeignKey(Carrier, null=True)

    def __str__(self):
        return "%s: %s" % (self.user.get_username(), self.phone_number)