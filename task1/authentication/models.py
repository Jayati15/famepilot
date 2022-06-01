import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, email, address="", dob=datetime.now() , phone="", password=None ):
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        if dob is None:
            raise TypeError('Users must have DOB.')

        if phone is None:
            raise TypeError('Users must have a phone number.')

        user = self.model(username=username, email=self.normalize_email(email),address=address, dob=dob, phone=phone)
        user.set_password(password)
        user.save()

        return user

    # for creating superuser
    def create_superuser(self, username, email, password):

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

# blueprint of user info i.e. how many column in their info
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    address = models.CharField(max_length=255)
    dob = models.DateField(auto_now=True)
    phone = models.CharField(max_length=10)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']    
    objects = UserManager()


    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(seconds=300)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s')),
            'username':self.username,
            'email':self.email
        }, settings.SECRET_KEY, algorithm='HS256')
        # print(token)
        # return token.decode('utf-8')
        return token