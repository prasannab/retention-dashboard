from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User

class NoNewUsersAccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        """
        Checks whether or not the site is open for signups.
        Next to simply returning True/False you can also intervene the
        regular flow by raising an ImmediateHttpResponse
        (Comment reproduced from the overridden method.)
        """
        return False

class MySocialAccount(DefaultSocialAccountAdapter):
    
    def pre_social_login(self, request, sociallogin):

        users = User.objects.all()
        print(users)

        u = sociallogin.user
        if not u.email.split('@')[1] == "freshworks.com":
            raise ImmediateHttpResponse(render_to_response('socialaccount/authentication_error.html'))
