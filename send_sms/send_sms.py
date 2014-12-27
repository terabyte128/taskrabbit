from django.core.mail import send_mail
import local_settings

__author__ = 'Sam'


def send_text_message(user, subject, message):

    phone_number = user.phonenumber.phone_number
    extension = user.phonenumber.carrier.email_extension

    phone_email = format("%s@%s" % (str(phone_number), extension))

    recipient_list = [
        phone_email
    ]

    send_mail(subject, message, local_settings.EMAIL_HOST_USER, recipient_list)

