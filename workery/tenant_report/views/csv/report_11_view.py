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


def report_11_streaming_csv_view(request):
    # Get our user parameters.
    naive_from_dt = request.GET.get('from_dt', None)
    naive_to_dt = request.GET.get('to_dt', None)

    # Convert our datatime `string` into a `datatime` object.
    naive_from_dt = parser.parse(naive_from_dt)
    naive_to_dt = parser.parse(naive_to_dt)

    # Convert our aware datetimes to the specific timezone of the tenant.
    today = timezone.now()
    tenant_today = request.tenant.to_tenant_dt(today)
    tenant_from_dt = request.tenant.localize_tenant_dt(naive_from_dt)
    tenant_from_d = tenant_from_dt.date()
    tenant_to_dt = request.tenant.localize_tenant_dt(naive_to_dt)
    tenant_to_d = tenant_to_dt.date()

    # Run our filter lookup.
    jobs = WorkOrder.objects.filter(
        assignment_date__range=(tenant_from_dt,tenant_to_dt),
        type_of=COMMERCIAL_JOB_TYPE_OF_ID,
        customer__isnull=False,
        associate__isnull=False
    ).order_by(
       '-id'
    ).prefetch_related(
        'customer',
        'associate',
        'skill_sets'
    )

    # Generate our new header.
    rows = (["Commercial Jobs Report","","",],)
    rows += (["Report Date:", pretty_dt_string(tenant_today),"",],)
    rows += (["From Assignment Date:", pretty_dt_string(tenant_from_d),"",],)
    rows += (["To Assignment Date:", pretty_dt_string(tenant_to_d),"",],)
    rows += (["", "","",],)
    rows += (["", "","",],)

    # Generate the CSV header row.
    rows += ([
        "Job No.",
        "Job Status",
        "Assignment",
        "Completion",
        "Associate No.",
        "Associate Company",
        "Associate",
        "Associate DOB",
        "Associate Age",
        "Client No.",
        "Client Company",
        "Client",
        "Client Birthdate",
        "Client Age",
        "WSIB #",
        "WSIB Date",
        "Total Labour",
        "Invoice #",
        "Skill Sets"
    ],)

    # Generate hte CSV data.
    for job in jobs.all():

        # Get our list of skill sets.
        skill_set_text = job.get_skill_sets_string()

        # Set the invoice ID.
        invoice_ids = "-" if job.invoice_ids is None else job.invoice_ids
        invoice_ids = "-" if job.invoice_ids is None else job.invoice_ids
        wsib_number = "-" if job.associate.wsib_number is None else job.associate.wsib_number
        wsib_insurance_date = "-" if job.associate.wsib_insurance_date is None else job.associate.wsib_insurance_date

        # Get our DOB and age.
        associate_id = None
        associate_dob = None
        associate_age = None
        if job.associate:
            associate_id = job.associate.id
            associate_dob = pretty_dt_string(job.associate.birthdate) if job.associate.birthdate is not None else ""
            associate_age = job.associate.get_current_age()
        customer_dob = pretty_dt_string(job.customer.birthdate) if job.customer.birthdate is not None else ""

        # Format labour amount
        invoice_labour_amount = str(job.invoice_labour_amount)
        invoice_labour_amount = invoice_labour_amount.replace('C', '')

        # Get the organization name.
        associate_company = job.associate.organization_name if job.associate.organization_name else "-"
        client_company = job.customer.organization_name if job.customer.organization_name else "-"

        # Generate the reason.
        rows += ([
            str(job.id),
            job.get_pretty_status(),
            pretty_dt_string(job.assignment_date),
            pretty_dt_string(job.completion_date),
            str(associate_id),
            associate_company,
            str(job.associate),
            associate_dob,
            associate_age,
            str(job.customer.id),
            client_company,
            str(job.customer),
            str(customer_dob),
            job.customer.get_current_age(),
            str(wsib_number),
            str(wsib_insurance_date),
            invoice_labour_amount,
            str(invoice_ids),
            skill_set_text,
        ],)

    # Create the virtual CSV file and stream all the data in real time to the
    # client.
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse(
        (writer.writerow(row) for row in rows),
        content_type="text/csv"
    )
    response['Content-Disposition'] = 'attachment; filename="commercial_jobs.csv"'
    return response
