# Python imports
from typing import Dict, Any

# django/rest_framwork imports
from model_utils import Choices
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MinValueValidator, MaxValueValidator

# app level imports
from .managers import UserManager


class User(AbstractBaseUser):
    """
    User model represents the user data in the database.
    """

    email = models.EmailField(max_length=128, db_index=True, unique=True)
    mobile = models.BigIntegerField(
        validators=[MinValueValidator(5000000000), MaxValueValidator(9999999999),],
        db_index=True,
        null=True,
    )
    is_staff = models.BooleanField(
        default=False,
    )
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    objects = UserManager()

    USERNAME_FIELD = "email"

    class Meta:
        app_label = "accounts"
        db_table = "twitter_user"

    def __str__(self):
        return str(self.email)

    def modify(self, payload: Dict[str, Any]):
        """
        This will update license object
        """
        for key, value in payload.items():
            setattr(self, key, value)
        self.save()


class Posts(models.Model):
    STATUS = Choices(
        (0, 'text', 'TEXT'), (1, 'image', 'IMAGE'), (2, 'video', 'VIDEO'),
    )
    user = models.ForeignKey('accounts.User', models.PROTECT,)
    type = models.IntegerField(choices=STATUS, default=STATUS.text)
    content = models.TextField(blank=False)

    class Meta:
        app_label = 'accounts'
        db_table = 'twitter_posts'


class Followers_Data(models.Model):
    follower_id = models.BigIntegerField()
    followee_id = models.BigIntegerField()

    class Meta:
        app_label = 'accounts'
        db_table = 'twitter_followers_data'


class Likes(models.Model):
    post = models.ForeignKey('accounts.Posts', models.PROTECT,)
    user = models.ForeignKey('accounts.User', models.PROTECT,)

    class Meta:
        app_label = 'accounts'
        db_table = 'twitter_likes'