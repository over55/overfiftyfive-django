# -*- coding: utf-8 -*-
import logging
import phonenumbers
from datetime import datetime, timedelta
from dateutil import tz
from djmoney.money import Money
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate
from django.db.models import Q, Prefetch, Sum
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.http import urlquote
from rest_framework import exceptions, serializers
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator

from shared_foundation.custom.drf.fields import PhoneNumberField
from shared_foundation.constants import CUSTOMER_GROUP_ID, WORKERY_APP_DEFAULT_MONEY_CURRENCY
from shared_foundation.models import SharedUser
from tenant_foundation.constants import *
from tenant_foundation.models import (
    Comment,
    ActivitySheetItem,
    Associate,
    WORK_ORDER_STATE,
    WorkOrder,
    WorkOrderComment,
    Organization,
    TaskItem
)


logger = logging.getLogger(__name__)


def get_todays_date_plus_days(days=0):
    """Returns the current date plus paramter number of days."""
    return timezone.now() + timedelta(days=days)


def cannot_be_zero_or_negative(value):
    if value <= 0:
        raise serializers.ValidationError('Please pick a reason from the dropdown.')
    return value


def cannot_be_negative(value):
    if value < 0:
        raise serializers.ValidationError('Please enter an amount which is not negative!')
    return value


#TODO: INTEGRATE


class CloseTaskOperationSerializer(serializers.Serializer):
    task_item = serializers.PrimaryKeyRelatedField(many=False, queryset=TaskItem.objects.all(), required=True)
    reason = serializers.IntegerField(required=False, validators=[cannot_be_zero_or_negative,])
    reason_other = serializers.CharField(required=False, allow_blank=True)
    additional_comment = serializers.CharField(required=False, allow_blank=True)
    was_job_satisfactory = serializers.BooleanField(required=False)
    was_job_finished_on_time_and_on_budget = serializers.BooleanField(required=False)
    was_associate_punctual = serializers.BooleanField(required=False)
    was_associate_professional = serializers.BooleanField(required=False)
    would_customer_refer_our_organization = serializers.BooleanField(required=False)
    invoice_date = serializers.DateField(required=False)
    invoice_ids = serializers.CharField(required=False)
    invoice_quote_amount = serializers.FloatField(required=False, validators=[cannot_be_negative,])
    invoice_labour_amount = serializers.FloatField(required=False, validators=[cannot_be_negative,])
    invoice_material_amount = serializers.FloatField(required=False, validators=[cannot_be_negative,])
    invoice_tax_amount = serializers.FloatField(required=False, validators=[cannot_be_negative,])
    invoice_total_amount = serializers.FloatField(required=False, validators=[cannot_be_negative,])
    invoice_service_fee_amount = serializers.FloatField(required=False, validators=[cannot_be_negative,])

    # Meta Information.
    class Meta:
        fields = (
            'task_item',
            'reason',
            'reason_other',
            'additional_comment',
            'was_job_satisfactory',
            'was_job_finished_on_time_and_on_budget',
            'was_associate_punctual',
            'was_associate_professional',
            'would_customer_refer_our_organization',
            'invoice_date',
            'invoice_ids',
            'invoice_quote_amount',
            'invoice_labour_amount',
            'invoice_material_amount',
            'invoice_tax_amount',
            'invoice_total_amount',
            'invoice_service_fee_amount'
        )

    def validate(self, data):
        """
        Override the validator to provide additional custom validation based
        on our custom logic.

        1. If 'reason' == 1 then make sure 'reason_other' was inputted.
        2. If 'reason' == 4 then make sure the Customer survey fields where inputted.
        """
        # CASE 1 - Other reason
        if data['reason'] == 1:
            reason_other = data['reason_other']
            if reason_other == "":
                raise serializers.ValidationError(_("Please provide a reason as to why you chose the \"Other\" option."))

        # CASE 2 - Job done by associate
        elif data['reason'] == 4:
            pass #TODO: IMPLEMENT.

        # Return our data.
        return data

    def create(self, validated_data):
        """
        Override the `create` function to add extra functinality.
        """
        #--------------------------#
        # Get validated POST data. #
        #--------------------------#
        task_item = validated_data.get('task_item', None)
        reason = validated_data.get('reason', None)
        reason_other = validated_data.get('reason_other', None)
        additional_comment_text = validated_data.get('additional_comment', None)
        was_job_satisfactory = validated_data.get('was_job_satisfactory', False)
        was_job_finished_on_time_and_on_budget = validated_data.get('was_job_finished_on_time_and_on_budget', False)
        was_associate_punctual = validated_data.get('was_associate_punctual', False)
        was_associate_professional = validated_data.get('was_associate_professional', False)
        would_customer_refer_our_organization = validated_data.get('would_customer_refer_our_organization', False)
        invoice_date = validated_data.get('invoice_date', None)
        invoice_ids = validated_data.get('invoice_ids',  0)
        invoice_quote_amount = validated_data.get('invoice_quote_amount',  0)
        invoice_labour_amount = validated_data.get('invoice_labour_amount',  0)
        invoice_material_amount = validated_data.get('invoice_material_amount',  0)
        invoice_tax_amount = validated_data.get('invoice_tax_amount',  0)
        invoice_total_amount = validated_data.get('invoice_total_amount',  0)
        invoice_service_fee_amount = validated_data.get('invoice_service_fee_amount',  0)

        # -------------------------
        # --- FINANCIAL DETAILS ---
        # -------------------------
        if task_item.job.closing_reason == 4:
            task_item.job.state = WORK_ORDER_STATE.COMPLETED_BUT_UNPAID
        else:
            task_item.job.state = WORK_ORDER_STATE.CANCELLED
        task_item.job.invoice_date = invoice_date
        task_item.job.invoice_ids = invoice_ids
        task_item.job.invoice_quote_amount = Money(invoice_quote_amount, WORKERY_APP_DEFAULT_MONEY_CURRENCY)
        task_item.job.invoice_labour_amount = Money(invoice_labour_amount, WORKERY_APP_DEFAULT_MONEY_CURRENCY)
        task_item.job.invoice_material_amount = Money(invoice_material_amount, WORKERY_APP_DEFAULT_MONEY_CURRENCY)
        task_item.job.invoice_tax_amount = Money(invoice_tax_amount, WORKERY_APP_DEFAULT_MONEY_CURRENCY)
        task_item.job.invoice_total_amount = Money(invoice_total_amount, WORKERY_APP_DEFAULT_MONEY_CURRENCY)
        task_item.job.invoice_service_fee_amount = Money(invoice_service_fee_amount, WORKERY_APP_DEFAULT_MONEY_CURRENCY)
        task_item.job.last_modified_by = self.context['user']
        task_item.job.last_modified_from = self.context['from']
        task_item.job.last_modified_from_is_public = self.context['from_is_public']
        task_item.job.save()

        # For debugging purposes only.
        logger.info("Job financials where updated.")

        #------------------------------------------#
        # Create any additional optional comments. #
        #------------------------------------------#
        if additional_comment_text:
            comment_obj = Comment.objects.create(
                created_by=self.context['user'],
                last_modified_by=self.context['user'],
                text=additional_comment_text,
                created_from = self.context['from'],
                created_from_is_public = self.context['from_is_public']
            )
            WorkOrderComment.objects.create(
                about=task_item.job,
                comment=comment_obj,
            )

            # For debugging purposes only.
            logger.info("Job comment created.")

        #----------------------------------------#
        # Lookup our Task(s) and close them all. #
        #----------------------------------------#
        task_items = TaskItem.objects.filter(
            job=task_item.job,
            is_closed=False
        )
        for task_item in task_items.all():
            logger.info("Found task # #%(id)s ." % {
                'id': str(task_item.id)
            })
            task_item.reason = reason
            task_item.reason_other = reason_other
            task_item.is_closed = True
            task_item.last_modified_by = self.context['user']
            task_item.save()
            logger.info("Task #%(id)s was closed." % {
                'id': str(task_item.id)
            })

        # ------------------------
        # --- JOB IS CANCELLED ---
        # ------------------------
        if reason != 4:
            # Close the job.
            task_item.job.closing_reason = reason
            task_item.job.closing_reason_other = reason_other
            task_item.job.last_modified_by = self.context['user']
            task_item.job.state = WORK_ORDER_STATE.CANCELLED
            task_item.job.completion_date = get_todays_date_plus_days(0)
            task_item.job.latest_pending_task = None
            task_item.job.save()

            # For debugging purposes only.
            logger.info("Job was cancelled.")

        # ---------------------
        # --- JOB IS CLOSED ---
        # ---------------------
        else:
            #---------------#
            # Close the job #
            #---------------#
            # STEP 1 - Close the job.
            task_item.job.closing_reason = reason
            task_item.job.closing_reason_other = reason_other
            task_item.job.last_modified_by = self.context['user']
            task_item.job.state = WORK_ORDER_STATE.COMPLETED_BUT_UNPAID
            task_item.job.completion_date = get_todays_date_plus_days(0)
            task_item.job.latest_pending_task = None

            # STEP 2 - Save the results.
            task_item.job.was_job_satisfactory = was_job_satisfactory
            task_item.job.was_job_finished_on_time_and_on_budget = was_job_finished_on_time_and_on_budget
            task_item.job.was_associate_punctual = was_associate_punctual
            task_item.job.was_associate_professional = was_associate_professional
            task_item.job.would_customer_refer_our_organization = would_customer_refer_our_organization

            #-------------------------#
            # Compute associate score #
            #-------------------------#
            # STEP 3 - Compute the score.
            task_item.job.score = 0
            task_item.job.score += int(was_job_satisfactory)
            task_item.job.score += int(was_job_finished_on_time_and_on_budget)
            task_item.job.score += int(was_associate_punctual)
            task_item.job.score += int(was_associate_professional)
            task_item.job.score += int(would_customer_refer_our_organization)
            task_item.job.save()

            # For debugging purposes only.
            logger.info("Job was completed.")

            # STEP 4 - Update the associate score by re-computing the average
            #          score and saving it with the profile.
            jobs_count = WorkOrder.objects.filter(
                Q(associate = task_item.job.associate) &
                Q(closing_reason = 4) &
                ~Q(state=WORK_ORDER_STATE.CANCELLED) &
                ~Q(state=WORK_ORDER_STATE.ARCHIVED)
            ).count()
            summation_results = WorkOrder.objects.filter(
                Q(associate = task_item.job.associate) &
                Q(closing_reason = 4) &
                ~Q(state=WORK_ORDER_STATE.CANCELLED) &
                ~Q(state=WORK_ORDER_STATE.ARCHIVED)
            ).aggregate(Sum('score'))

            score_sum = summation_results['score__sum']
            total_score = score_sum / jobs_count

            # For debugging purposes only.
            logger.info("Assocate is calculated as: %(total_score)s" % {
                'total_score': str(total_score)
            })

        #--------------------------------#
        # Update our `OngoingWorkOrder`. #
        #--------------------------------#
        if task_item.job.ongoing_work_order:
            task_item.job.ongoing_work_order.save()
            task_item.job.ongoing_work_order.closed_orders.add(task_item.job)

        #--------------------#
        # Updated the output #
        #--------------------#
        # validated_data['id'] = obj.id
        return validated_data
