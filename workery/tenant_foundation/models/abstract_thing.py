# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from shared_foundation.models.user import SharedUser


class AbstractThing(models.Model):
    """
    The most generic type of item.

    https://schema.org/Thing
    """
    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        SharedUser,
        help_text=_('The user whom owns this thing.'),
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_abstract_thing_owner_related",
        on_delete=models.CASCADE
    )
    alternate_name = models.CharField(
        _("Alternate Name"),
        max_length=255,
        help_text=_('An alias for the item.'),
        blank=True,
        null=True,
    )
    description = models.TextField(
        _("Description"),
        help_text=_('A short description of the item.'),
        blank=True,
        null=True,
        default='',
    )
    # image = models.ForeignKey(
    #     ImageUpload,
    #     help_text=_('An image of the item.'),
    #     null=True,
    #     blank=True,
    #     related_name="abstract_thing_image_%(app_label)s_%(class)s_related",
    #     on_delete=models.SET_NULL
    # )
    # main_entity_of_page = models.URLField(
    #     _("Main Entity Of Page"),
    #     help_text=_('Indicates a page for which this thing is the main entity being described.'),
    #     null=True,
    #     blank=True
    # )
    name = models.CharField(
        _("Name"),
        max_length=255,
        help_text=_('The name of the item.'),
        blank=True,
        null=True,
        default='',
        db_index=True,
    )
    # same_as = models.URLField(
    #     _("Same As"),
    #     help_text=_('URL of a reference Web page that unambiguously indicates the item\'s identity. E.g. the URL of the item\'s Wikipedia page, Freebase page, or official website.'),
    #     null=True,
    #     blank=True
    # )
    url = models.URLField(
        _("URL"),
        help_text=_('URL of the item.'),
        null=True,
        blank=True
    )
