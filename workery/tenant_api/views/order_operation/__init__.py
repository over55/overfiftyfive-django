# -*- coding: utf-8 -*-
from tenant_api.views.order_operation.order_clone import WorkOrderCloneOperationCreateAPIView
from tenant_api.views.order_operation.order_close import WorkOrderCloseOperationCreateAPIView
from tenant_api.views.order_operation.order_unassign import WorkOrderUnassignOperationCreateAPIView
from tenant_api.views.order_operation.order_postpone import WorkOrderPostponeOperationCreateAPIView
from tenant_api.views.order_operation.order_reopen import WorkOrderReopenOperationCreateAPIView
from tenant_api.views.order_operation.transfer_work import TransferWorkerOrderOperationAPIView
from tenant_api.views.order_operation.order_invoice import WorkOrderInvoiceCreateOrUpdateOperationAPIView
