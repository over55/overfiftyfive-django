# -*- coding: utf-8 -*-
from tenant_api.views.order_operation.ongoing_order_close import OngoingWorkOrderCloseOperationAPIView
from tenant_api.views.order_operation.ongoing_order_unassign import OngoingWorkOrderUnassignOperationAPIView
from tenant_api.views.order_operation.order_close import (
    CompletedWorkOrderCloseOperationCreateAPIView,
    IncompleteWorkOrderCloseOperationCreateAPIView
)
from tenant_api.views.order_operation.order_unassign import WorkOrderUnassignOperationCreateAPIView
from tenant_api.views.order_operation.order_postpone import WorkOrderPostponeOperationCreateAPIView
from tenant_api.views.order_operation.order_reopen import WorkOrderReopenOperationCreateAPIView
