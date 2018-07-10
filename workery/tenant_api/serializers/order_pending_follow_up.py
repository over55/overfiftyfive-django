# -*- coding: utf-8 -*-
import logging
import phonenumbers
from datetime import datetime, timedelta
from dateutil import tz
from starterkit.drf.validation import (
    MatchingDuelFieldsValidator,
    EnhancedPasswordStrengthFieldValidator
)
from starterkit.utils import (
    get_random_string,
    get_unique_username_from_email
)
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate
from django.db.models import Q, Prefetch
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.http import urlquote
from rest_framework import exceptions, serializers
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from shared_api.custom_fields import PhoneNumberField
from shared_foundation.constants import CUSTOMER_GROUP_ID
from shared_foundation.models import SharedUser
from tenant_foundation.constants import *
from tenant_foundation.models import (
    Comment,
    ACTIVITY_SHEET_ITEM_STATE,
    ActivitySheetItem,
    Associate,
    WorkOrder,
    WORK_ORDER_STATE,
    WorkOrderComment,
    Organization,
    TaskItem
)


logger = logging.getLogger(__name__)


def get_todays_date_plus_days(days=0):
    """Returns the current date plus paramter number of days."""
    return timezone.now() + timedelta(days=days)


class PendingFollowUpCreateSerializer(serializers.Serializer):
    job = serializers.PrimaryKeyRelatedField(many=False, queryset=WorkOrder.objects.all(), required=True)
    associate = serializers.PrimaryKeyRelatedField(many=False, queryset=Associate.objects.all(), required=True)
    comment = serializers.CharField(required=True)
    state = serializers.CharField(
        required=True,
        error_messages={
            "invalid": "Please pick either 'Yes', 'No', or 'Pending' choice."
        }
    )

    # Meta Information.
    class Meta:
        fields = (
            'job',
            'associate',
            'comment',
            'state',
        )

    def validate(self, data):
        """
        Override the final validation to include additional extras. Any
        validation error will be populated in the "non_field_errors" field.
        """
        # Confirm that we have an assignment task open.
        task_item = TaskItem.objects.filter(
            type_of=FOLLOW_UP_DID_ASSOCIATE_ACCEPT_JOB_TASK_ITEM_TYPE_OF_ID,
            job=data['job'],
            is_closed=False
        ).order_by('due_date').first()
        if task_item is None:
            raise serializers.ValidationError(_("Task no longer exists, please go back to the list page."))
        return data

    def create(self, validated_data):
        """
        Override the `create` function to add extra functinality.
        """
        # STEP 1 - Get validated POST data.
        job = validated_data.get('job', None)
        associate = validated_data.get('associate', None)
        comment = validated_data.get('comment', None)
        state = validated_data.get('state', None)

        # STEP 2 - Lookup the most recent task which has not been closed
        #          for the particular job order.
        task_item = TaskItem.objects.filter(
            type_of=FOLLOW_UP_DID_ASSOCIATE_ACCEPT_JOB_TASK_ITEM_TYPE_OF_ID,
            job=job,
            is_closed=False
        ).order_by('due_date').first()

        # For debugging purposes only.
        logger.info("Found task #%(task_item)s" % {
            'task_item': str(task_item.id)
        })

        # STEP 3 - Update our TaskItem to be closed.
        task_item.is_closed = True
        task_item.last_modified_by = self.context['user']
        task_item.save()

        # For debugging purposes only.
        logger.info("Task #%(task_item)s was closed." % {
            'task_item': str(task_item.id)
        })

        # STEP 4 - Lookup our current activity sheet and set the status of
        #          the activity sheet based on the users decision.
        current_activity_sheet_item = ActivitySheetItem.objects.filter(
            job=job,
            associate=associate,
        ).first()
        current_activity_sheet_item.state = state
        current_activity_sheet_item.last_modified_by = self.context['user']
        current_activity_sheet_item.save()

        if state == ACTIVITY_SHEET_ITEM_STATE.ACCEPTED or state == ACTIVITY_SHEET_ITEM_STATE.PENDING:
            '''
            Accepted or Pending
            '''

            # STEP 5 - Update our job.
            current_activity_sheet_item.job.associate = associate
            current_activity_sheet_item.job.assignment_date = get_todays_date_plus_days()
            current_activity_sheet_item.job.save()

            # For debugging purposes only.
            logger.info("Associate assigned to Job.")

            # Create the task message / time based on the `state`.
            title = None
            description = None
            due_date = None
            type_of = None
            if state == ACTIVITY_SHEET_ITEM_STATE.ACCEPTED:
                title = _('48 hour follow up')
                description = _('Please call up the client and confirm that the associate and client have agreed on scheduled meeting date in the future.')
                due_date = get_todays_date_plus_days(2)
                type_of = FOLLOW_UP_IS_JOB_COMPLETE_TASK_ITEM_TYPE_OF_ID
            elif state == ACTIVITY_SHEET_ITEM_STATE.PENDING:
                title = _('Pending')
                description = _('Please contact the Associate to confirm if they want the job.')
                due_date = get_todays_date_plus_days(1)
                type_of = FOLLOW_UP_DID_ASSOCIATE_ACCEPT_JOB_TASK_ITEM_TYPE_OF_ID

            # STEP 6 - Create our new task for following up.
            next_task_item = TaskItem.objects.create(
                type_of = type_of,
                title = title,
                description = description,
                due_date = due_date,
                is_closed = False,
                job = task_item.job,
                created_by = self.context['user'],
                last_modified_by = self.context['user']
            )

            # For debugging purposes only.
            logger.info("Task #%(id)s was created." % {
                'id': str(next_task_item.id)
            })

            # Attached our new TaskItem to the Job.
            job.latest_pending_task = next_task_item

            # Change state
            if state == ACTIVITY_SHEET_ITEM_STATE.ACCEPTED:
                job.state = WORK_ORDER_STATE.IN_PROGRESS
            if state == ACTIVITY_SHEET_ITEM_STATE.PENDING:
                job.state = WORK_ORDER_STATE.PENDING

            # Save our new task and job state updated.
            job.save()

        else:
            '''
            Declined
            '''

            #---------------------------------------------#
            # Create a new task based on a new start date #
            #---------------------------------------------#
            next_task_item = TaskItem.objects.create(
                created_by=self.context['user'],
                last_modified_by=self.context['user'],
                type_of = ASSIGNED_ASSOCIATE_TASK_ITEM_TYPE_OF_ID,
                due_date = job.start_date,
                is_closed = False,
                job = job,
                title = _('Assign an Associate'),
                description = _('Please assign an associate to this job.')
            )

            # For debugging purposes only.
            logger.info("Assignment Task #%(id)s was created b/c of unassignment." % {
                'id': str(next_task_item.id)
            })

            # Attach our next job.
            job.associate = None
            job.state = WORK_ORDER_STATE.DECLINED
            job.latest_pending_task = next_task_item
            job.save()

        # STEP 5 - Assign our new variables and return the validated data.
        validated_data['id'] = current_activity_sheet_item.id
        return validated_data
