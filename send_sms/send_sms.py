from django.core.mail import send_mail
import local_settings
from send_sms.models import PhoneNumber

__author__ = 'Sam'


def send_text_message(user, subject, message):

    phone_number = user.phonenumber.phone_number
    extension = user.phonenumber.carrier.email_extension

    phone_email = format("%s@%s" % (str(phone_number), extension))

    recipient_list = [
        phone_email
    ]

    send_mail(subject, message, local_settings.EMAIL_HOST_USER, recipient_list)


def has_email(user):
    try:
        num = user.phonenumber
        return True
    except PhoneNumber.DoesNotExist:
        return False