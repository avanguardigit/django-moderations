from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend


class BlockBannedUserBackend(ModelBackend):
    def user_can_authenticate(self, user):
        if user.is_ban:
            return False
        else:
            return True
