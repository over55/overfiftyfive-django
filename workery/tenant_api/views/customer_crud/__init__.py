# -*- coding: utf-8 -*-
from tenant_api.views.customer_crud.customer_list_create_view import CustomerListCreateV2APIView
from tenant_api.views.customer_crud.customer_retrieve_update_destroy import CustomerRetrieveUpdateDestroyV2APIView
from tenant_api.views.customer_crud.customer_file_upload import (
    CustomerFileUploadListCreateAPIView,
    CustomerFileUploadArchiveAPIView
)
from tenant_api.views.customer_crud.customer_contact_update import CustomerContactUpdateAPIView
from tenant_api.views.customer_crud.customer_address_update import CustomerAddressUpdateAPIView
from tenant_api.views.customer_crud.customer_metrics_update import CustomerMetricsUpdateAPIView
