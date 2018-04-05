from django.conf.urls import include, url
from django.urls import path
from django.views.generic.base import RedirectView
from tenant_customer.views import create_view, list_view, retrieve_view, search_view, update_view


urlpatterns = (
    # Summary
    path('clients/', list_view.CustomerSummaryView.as_view(), name='o55_tenant_customer_summary'),

    # Create
    path('clients/create/', create_view.CustomerCreateView.as_view(), name='o55_tenant_customer_create'),

    # List
    path('clients/list/', list_view.CustomerListView.as_view(), name='o55_tenant_customer_list'),

    # Search
    path('clients/search/', search_view.CustomerSearchView.as_view(), name='o55_tenant_customer_search'),
    path('clients/search/results/', search_view.CustomerSearchResultView.as_view(), name='o55_tenant_customer_search_results'),

    # Retrieve
    path('clients/detail/<str:template>/<int:pk>/', retrieve_view.CustomerRetrieveView.as_view(), name='o55_tenant_customer_retrieve'),

    # Update
    path('clients/detail/<str:template>/<int:pk>/edit/', update_view.CustomerUpdateView.as_view(), name='o55_tenant_customer_update'),
)
