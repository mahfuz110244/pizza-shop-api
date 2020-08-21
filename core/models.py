from django.db import models
from user.models import Customer


class BaseModel(models.Model):
    created_by = models.ForeignKey(Customer, related_name='%(class)s_created_by', on_delete=models.DO_NOTHING,
                                   blank=True, null=True)
    updated_by = models.ForeignKey(Customer, related_name='%(class)s_updated_by', on_delete=models.DO_NOTHING,
                                   blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    inactive = models.BooleanField(default=False, blank=True, null=True)
    deleted = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        abstract = True
