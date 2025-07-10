from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from .models import CustomUser, Invitation

@shared_task
def send_activation_email(user_id):
    user = CustomUser.objects.get(pk=user_id)
    token = settings.EMAIL_VERIFICATION_TOKEN_GENERATOR.make_token(user)
    link = f"{settings.SITE_URL}{reverse('accounts-activate', args=[user.pk, token])}"
    subject = 'Verify your email'
    body = render_to_string('accounts/email/activation.html', {'user': user, 'link': link})
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email])

@shared_task
def send_invitation_email(invitation_id):
    invitation = Invitation.objects.get(pk=invitation_id)
    subject = f"{invitation.role} invitation to EduTrace"
    body = f"Use this invite code to register: {invitation.code}"
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [invitation.email])
