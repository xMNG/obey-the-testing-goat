# from django.core.exceptions import ValidationError
# from accounts.models import Token, User
#
#
# class PasswordlessAuthenticationBackend(object):
#
#     def authenticate(self, uid):
#         """
#
#         :param uid:
#         :return: Returns user (current or created new user) if valid uid, else returns None
#         """
#         try:
#             token = Token.objects.get(uid=uid)
#             return User.objects.get(email=token.email)
#         except (Token.DoesNotExist, ValidationError):
#             return None
#         except User.DoesNotExist:
#             return User.objects.create(email=token.email)
#
#     def get_user(self, email):
#         try:
#             return User.objects.get(email=email)
#         except User.DoesNotExist:
#             return None

from accounts.models import User, Token

class PasswordlessAuthenticationBackend(object):

    def authenticate(self, uid):
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            return User.objects.create(email=token.email)
        except Token.DoesNotExist:
            return None


    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

