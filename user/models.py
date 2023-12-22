import uuid as uuid
from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        ordering = ('id',)

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='user/images/', null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)

    def delete(self, using=None, keep_parents=False):
        """
        Soft deletes the user by setting the 'is_delete' flag to True.
        The user record is not removed from the database, only marked as deleted.
        """

        self.is_delete = True
        self.save()

    def erase(self, **kwargs):
        """
        Permanently deletes the user from the database.
        This operation is irreversible and removes the user record from the database.
        Actually delete from database.
        """
        return super().delete(**kwargs)
