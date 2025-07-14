from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from .models import CustomUser, Invitation
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@shared_task
def send_activation_email(user_id):
    user = CustomUser.objects.get(pk=user_id)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = settings.EMAIL_VERIFICATION_TOKEN_GENERATOR.make_token(user)
    link = f"{settings.SITE_URL}{reverse('accounts-activate', args=[uidb64, token])}"
    subject = 'Verify your email'
    html_content = render_to_string('accounts/email/activation.html', {'user': user, 'link': link})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
    email.attach_alternative(html_content, "text/html")
    email.send()
@shared_task
def send_invitation_email(invitation_id):
    invitation = Invitation.objects.get(pk=invitation_id)
    subject = f"{invitation.role} invitation to EduTrace"
    body = f"Use this invite code to register: {invitation.code}"
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [invitation.email])
