from django.contrib import admin
from .models import CustomUser, Invitation
from .tasks import send_invitation_email

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ['email', 'first_name', 'last_name']
    list_display = ('username', 'email', 'role', 'is_email_verified', )
    list_filter = ('role', 'is_email_verified', )

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('email', 'school', 'role', 'code', 'used', 'created')
    list_filter = ('school', 'role', 'used')
    actions = ['generate_and_send_invitations']

    def generate_and_send_invitations(self, request, queryset):
        for invitation in queryset:
            if not invitation.used:
                send_invitation_email.delay(invitation.id)
        self.message_user(request, "Invitation emails have been sent.")
