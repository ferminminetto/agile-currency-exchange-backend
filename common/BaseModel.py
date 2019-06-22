from django.db import models


class BaseManager(models.Manager):

    def get_queryset(self):
        return super(BaseManager, self).get_queryset().exclude(deleted=True)


class BaseModel(models.Model):
    """
    Core Base Model that adds soft deleting logic and log attributes.
    """

    class Meta:
        abstract = True

    objects = BaseManager()
    with_thrashed = models.Manager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def delete(self):
        self.deleted = True
        self.save()
