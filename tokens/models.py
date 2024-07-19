from django.db import models


class BlacklistedTokenManager(models.Manager):
    def add_token(self, token):
        return self.create(token=token)


class BlacklistedToken(models.Model):
    token = models.CharField(max_length=255)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    objects = BlacklistedTokenManager()

    def __str__(self):
        return self.token
