from django.db.models.signals import post_save
from django.dispatch import receiver

from tenant_foundation.models import Staff, UnifiedSearchItem


@receiver(post_save, sender=Staff)
def save_staff(sender, instance, **kwargs):
    """
    Function will either update or create the `UnifiedSearchItem` object so
    we have a unified searchable record for all our data.
    """
    UnifiedSearchItem.objects.update_or_create_staff(instance)
