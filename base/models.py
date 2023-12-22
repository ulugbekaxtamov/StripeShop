from django.utils import timezone
import uuid
from django.db import models
from user.models import User


class BaseModelManager(models.Manager):
    """
    Custom model manager for handling non-deleted objects.
    Overrides the default queryset to exclude logically deleted objects.
    """

    def get_queryset(self, *args, **kwargs):
        # Filter the queryset to exclude objects marked as deleted.
        return super().get_queryset(*args, **kwargs).filter(is_delete=False)


class DeleteBaseModelManager(models.Manager):
    """
    Custom model manager for handling logically deleted objects.
    Overrides the default queryset to include only logically deleted objects.
    """

    def get_queryset(self, *args, **kwargs):
        # Filter the queryset to include only objects marked as deleted.
        return super().get_queryset(*args, **kwargs).filter(is_delete=True)


class AllBaseModelManager(models.Manager):
    """
    Custom model manager for handling all objects without a logical delete filter.
    Returns the complete queryset including both deleted and non-deleted objects.
    """

    def get_queryset(self, *args, **kwargs):
        # Return the complete queryset without filtering for deletion status.
        return super().get_queryset(*args, **kwargs)


class Base(models.Model):
    """
    Abstract base model providing common fields and soft delete functionality.

    Attributes:
        created_at (DateTimeField): The date and time when the record was created.
        updated_at (DateTimeField): The date and time when the record was last updated.
        deleted_at (DateTimeField): The date and time when the record was marked as deleted.
        is_delete (BooleanField): Flag indicating whether the record is logically deleted.
        uuid (UUIDField): A unique identifier for the record.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_delete = models.BooleanField(default=False)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING)

    # Custom managers for different queryset filtering
    objects = BaseModelManager()
    delete_objects = DeleteBaseModelManager()
    all_objects = AllBaseModelManager()

    class Meta:
        abstract = True  # Indicates that this is an abstract base class

    def delete(self, using=None, keep_parents=False):
        """
        Soft delete method. Marks the object as deleted and sets the deleted timestamp
        without actually removing it from the database.
        """
        self.is_delete = True
        self.deleted_at = timezone.now()
        # Also soft delete all related objects
        for relation in self._meta._relation_tree:
            filter_kwargs = {relation.name: self}
            for obj in relation.model.objects.filter(**filter_kwargs):
                obj.delete()
        self.save()

    def restore(self, *args, **kwargs):
        """
        Restore a soft-deleted object, marking it as not deleted and updating the restored timestamp.
        """
        self.is_delete = False
        self.deleted_at = None  # Clearing the deleted timestamp
        # Also restore all related objects
        for relation in self._meta._relation_tree:
            filter_kwargs = {relation.name: self}
            for obj in relation.model.objects.filter(**filter_kwargs):
                obj.restore()
        self.save()

    def erase(self, **kwargs):
        """
        Permanently delete the object from the database.
        This is an irreversible operation.
        """
        return super().delete(**kwargs)
