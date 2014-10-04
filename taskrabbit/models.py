from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.


class Team(models.Model):
    name = models.TextField(max_length=128)
    description = models.TextField(max_length=500, blank=True)
    color = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.TextField(max_length=100)

    def __str__(self):
        return self.name


class Task(models.Model):
    owner = models.ForeignKey(User, related_name='owner', blank=True, null=True)

    name = models.TextField(max_length=256)
    description = models.TextField(max_length=500, blank=True)

    creation_date = models.DateField(default=datetime.date.today())
    last_worked_on = models.DateTimeField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)

    team = models.ForeignKey(Team)
    status = models.ForeignKey(Status, related_name='status')

    def __str__(self):
        return self.name


class Note(models.Model):
    task = models.ForeignKey(Task, related_name='task')
    user = models.ForeignKey(User, related_name='user')
    content = models.TextField(max_length=500)
    timestamp = models.DateTimeField(default=datetime.datetime.now())
    status = models.ForeignKey(Status, related_name='note_status')


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    team = models.ForeignKey(Team)


