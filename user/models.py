from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import jwt, datetime

class CustomUser(AbstractUser):
    address = models.TextField(blank=True, null=True)
    

    @property
    def generate_jwt_token(self):
        print(self.id)
        payload = {
            'id': self.id,
            'exp': datetime.datetime.now() + datetime.timedelta(minutes=5),
            'iat': datetime.datetime.now()
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        
        jwt_token = { 'token' : token, "expires_at" : payload['exp'] }

        return jwt_token

    @property
    def jwtToken(self):         
        return self.generate_jwt_token


