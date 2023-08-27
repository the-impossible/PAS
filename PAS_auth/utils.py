# My django imports
import threading #for enhancing page functionality
from django.core.mail import send_mail #for sending mails
from django.conf import settings #to gain access to variables from the settings
from django.http import request #to gain access to the request object
from django.views import View
from django.shortcuts import redirect, render
from django.urls import reverse
from django.template.loader import get_template #used for getting html template
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.contrib import messages #for sending messages
from django.conf import settings

# My App imports

class EmailThread(threading.Thread):
    def __init__(self, email_subject, email_body, receiver):
        self.email_subject = email_subject
        self.email_body = email_body
        self.sender = settings.EMAIL_HOST_USER
        self.receiver = receiver
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.email_subject,
            self.email_body,
            self.sender,
            self.receiver,
            html_message=self.email_body,
            fail_silently=False
        )

class AppTokenGenerator(PasswordResetTokenGenerator):
    def __make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.id)+text_type(timestamp))

email_activation_token = AppTokenGenerator()

class Mailer(View):


    def send(self, user_details, which):
        reset = 'Reset Your PROJECT Manager Account Password'
        activate = 'Verify Your PROJECT Manager Email Address'

        if which == 'reset':
            link = reverse('auth:complete_reset_password', kwargs={'uidb64':user_details['uid'], 'token':user_details['token']})
            activation_url = settings.HTTP+user_details['domain']+link
            activation_path = 'auth/verify_email.html'
            receiver = [user_details['email']]
            email_subject = reset
            context_data = {'type':'reset', 'user': user_details['fullname'], 'activate': activation_url}
            email_body = get_template(activation_path).render(context_data)
            EmailThread(email_subject, email_body, receiver).start()

        elif which == 'verify':
            link = reverse('auth:verify', kwargs={'uidb64':user_details['uid'], 'token':user_details['token']})
            activation_url = settings.HTTP+user_details['domain']+link
            activation_path = 'auth/verify_email.html'
            receiver = [user_details['email']]
            email_subject = activate
            context_data = {'type':'verify', 'user': user_details['fullname'], 'activate': activation_url}
            email_body = get_template(activation_path).render(context_data)
            EmailThread(email_subject, email_body, receiver).start()
        else:
            messages.error(request, 'Unable to process verification')

Email = Mailer()