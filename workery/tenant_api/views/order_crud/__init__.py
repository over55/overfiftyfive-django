# -*- coding: utf-8 -*-
from tenant_api.views.order_crud.order import (
   WorkOrderListCreateAPIView,
   WorkOrderRetrieveUpdateDestroyAPIView
)
from tenant_api.views.order_crud.order_comment import WorkOrderCommentListCreateAPIView
from tenant_api.views.order_crud.ongoing_order import (
   OngoingWorkOrderListCreateAPIView,
   OngoingWorkOrderRetrieveUpdateDestroyAPIView
)
from tenant_api.views.order_crud.ongoing_order_comment import OngoingWorkOrderCommentListCreateAPIView
from tenant_api.views.order_crud.order_lite_update import WorkOrderLiteUpdateAPIView
from tenant_api.views.order_crud.order_financial_update import WorkOrderFinancialUpdateAPIView
from tenant_api.views.order_crud.v2_ongoing_order import (
   OngoingWorkOrderListCreateV2APIView,
   OngoingWorkOrderRetrieveUpdateDestroyV2APIView
)
from tenant_api.views.order_crud.order_file_upload import (
    WorkOrderFileUploadListCreateAPIView,
    WorkOrderFileUploadArchiveAPIView
)
from tenant_api.views.order_crud.my_order_list_retrieve import (
    MyWorkOrderListAPIView,
    MyWorkOrderRetrieveAPIView
)
from tenant_api.views.order_crud.invoice_download_pdf import WorkOrderInvoiceDownloadPDFAPIView
from tenant_api.views.order_crud.invoice_retrieve import WorkOrderInvoiceRetrieveAPIView
from tenant_api.views.order_crud.invoice_first_section_update import WorkOrderInvoiceFirstSectionUpdateAPIView
from tenant_api.views.order_crud.invoice_second_section_update import WorkOrderInvoiceSecondSectionUpdateAPIView
from tenant_api.views.order_crud.invoice_third_section_update import WorkOrderInvoiceThirdSectionUpdateAPIView
from tenant_api.views.order_crud.deposit_list_create import WorkOrderDepositListCreateAPIView
from tenant_api.views.order_crud.deposit_delete import WorkOrderDepositDeleteAPIView
