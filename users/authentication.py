# import logging
# from django.contrib.auth.backends import BaseBackend
# from django.contrib.auth import get_user_model
#
#
#
# class EmailBackend(BaseBackend):
#     def authenticate(self, request, email=None, password=None, **kwargs):
#         User = get_user_model()
#         try:
#             user = User.objects.get(email=email)
#             logger.debug(f'User found: {user.email}')
#         except User.DoesNotExist:
#             logger.debug(f'User with email {email} does not exist.')
#             return None
#
#         if user.check_password(password):
#             logger.debug('Password is correct')
#             return user
#         else:
#             logger.debug('Password is incorrect')
#         return None
#
#     def get_user(self, user_id):
#         User = get_user_model()
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None
