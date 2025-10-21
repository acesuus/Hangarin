from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email, user_field, user_username
from allauth.utils import valid_email_or_none

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_auto_signup_allowed(self, request, sociallogin):
        # If email exists in database, don't allow auto signup
        email = valid_email_or_none(sociallogin.user.email)
        if email:
            return False
        return True

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        if not user.email:
            email = sociallogin.account.extra_data.get('email')
            if email:
                user_email(user, email)
        if not user.username:
            username = sociallogin.account.extra_data.get('login')  # GitHub specific
            if username:
                user_username(user, username)
        return user