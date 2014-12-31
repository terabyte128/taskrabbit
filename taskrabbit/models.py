import uuid
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
import local_settings


class Team(models.Model):
    name = models.TextField(max_length=128)
    description = models.TextField(max_length=500, blank=True)
    color = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Status(models.Model):

    name = models.TextField(max_length=100)
    show_in_table = models.BooleanField(default=True, verbose_name="Show as active")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Statuses"


class Task(models.Model):
    owner = models.ForeignKey(User, related_name='owner', blank=True, null=True)

    name = models.TextField(max_length=256)
    description = models.TextField(max_length=500, blank=True)

    start_date = models.DateField(default=datetime.date.today)
    last_worked_on = models.DateTimeField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    team = models.ForeignKey(Team)
    status = models.ForeignKey(Status, related_name='status')

    def __str__(self):
        return self.name

    def overdue(self):
        if self.end_date < datetime.date.today():
            return True
        return False


class Note(models.Model):
    task = models.ForeignKey(Task, related_name='task')
    user = models.ForeignKey(User, related_name='user')
    content = models.TextField(max_length=500)
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    status = models.ForeignKey(Status, related_name='note_status')

    automatic_note = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    team = models.ForeignKey(Team)


class TimeLog(models.Model):
    user = models.ForeignKey(User)
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField(null=True)
    time_length = models.DateTimeField(null=True)
    valid = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_full_name() + " @ " + str(self.entry_time)


class NfcCard(models.Model):
    user = models.ForeignKey(User)
    card_name = models.CharField(max_length=64)
    serial_number = models.CharField(max_length=64)
    secret_key = models.CharField(max_length=64)


def add_1_day():
    return datetime.datetime.now() + datetime.timedelta(days=1)


def get_random_id():
    return uuid.uuid4().hex


class AccountCreationID(models.Model):
    uuid = models.TextField(default=get_random_id)
    expire_date = models.DateTimeField(default=add_1_day)
    email_address = models.TextField(max_length=128, null=True)
    active = models.BooleanField(default=True)

    def save(self):
        if self.active:
            email_url = local_settings.SITE_URL + reverse('taskrabbit:create_account', kwargs={'creation_id': self.uuid})
            
            send_mail("Invite to create TaskRabbit Account", "You have been invited to create an account on TaskRabbit!"
                                                             "\nTo get started, click the link below."
                                                             "\n\n"
                                                             + email_url, local_settings.EMAIL_HOST_USER, [self.email_address])
            
        super(AccountCreationID, self).save()
