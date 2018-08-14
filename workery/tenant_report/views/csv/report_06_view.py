# -*- coding: utf-8 -*-
import datetime
from dateutil import parser
from djmoney.money import Money
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Extract
from django.db.models import Q
from django.views.generic import DetailView, ListView, TemplateView
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from shared_foundation.constants import *
from shared_foundation.mixins import ExtraRequestProcessingMixin
from shared_foundation.utils import *
from tenant_api.filters.customer import CustomerFilter
from tenant_foundation.constants import *
from tenant_foundation.models import (
    Associate,
    AwayLog,
    Customer,
    WORK_ORDER_STATE,
    WorkOrder,
    TaskItem,
    SkillSet
)

"""
Code below was taken from:
https://docs.djangoproject.com/en/2.0/howto/outputting-csv/
"""

import csv
from django.http import StreamingHttpResponse

class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def report_06_streaming_csv_view(request):
    today = timezone.now()
    associates = Associate.objects.filter(
        Q(owner__is_active=True)
    ).order_by('-police_check')

    # Convert our aware datetimes to the specific timezone of the tenant.
    tenant_today = request.tenant.to_tenant_dt(today)

    # Generate our new header.
    rows = (["Associate Police Check Due Dates","","",],)
    rows += (["Report Date:", pretty_dt_string(tenant_today),"",],)
    rows += (["", "","",],)
    rows += (["", "","",],)

    # Generate the CSV header row.
    rows += (["Associate No.", "Name", "Police Check Due Dates"],)

    # Generate hte CSV data.
    for associate in associates.all():
        rows += ([
            associate.id,
            str(associate),
            "-" if associate.police_check is None else pretty_dt_string(associate.police_check)
        ],)

    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse(
        (writer.writerow(row) for row in rows),
        content_type="text/csv"
    )
    response['Content-Disposition'] = 'attachment; filename="associate_policy_check_due_dates.csv"'
    return response
