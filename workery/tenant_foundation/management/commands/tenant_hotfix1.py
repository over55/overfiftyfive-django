# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError
from django.db import connection # Used for django tenants.
from django.utils.translation import ugettext_lazy as _
from starterkit.utils import (
    get_random_string,
    get_unique_username_from_email
)
from shared_foundation import constants
from shared_foundation.models import (
    SharedUser,
    SharedFranchise
)
from tenant_foundation.models import (
    ACTIVITY_SHEET_ITEM_STATE,
    ActivitySheetItem
)
from tenant_foundation.utils import *


class Command(BaseCommand):
    help = _('Command will transition fields.')

    def add_arguments(self, parser):
        """
        Run manually in console:
        python manage.py tenant_hotfix1 "london"
        """
        parser.add_argument('schema_name', nargs='+', type=str)

    def handle(self, *args, **options):
        # Connection needs first to be at the public schema, as this is where
        # the database needs to be set before creating a new tenant. If this is
        # not done then django-tenants will raise a "Can't create tenant outside
        # the public schema." error.
        connection.set_schema_to_public() # Switch to Public.
        # Get the user inputs.
        schema_name = options['schema_name'][0]

        try:
            franchise = SharedFranchise.objects.get(schema_name=schema_name)
        except SharedFranchise.DoesNotExist:
            raise CommandError(_('Franchise does not exist!'))

        # Connection will set it back to our tenant.
        connection.set_schema(franchise.schema_name, True) # Switch to Tenant.

        items = ActivitySheetItem.objects.all()
        for item in items.all():
            if item.has_accepted_job:
                item.state = ACTIVITY_SHEET_ITEM_STATE.ACCEPTED
            else:
                item.state = ACTIVITY_SHEET_ITEM_STATE.DECLINED
            item.save()

        # For debugging purposes.
        self.stdout.write(
            self.style.SUCCESS(_('Successfully changed work order.'))
        )
