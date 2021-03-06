# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from shared_foundation import constants
from shared_foundation.mixins import (
    ExtraRequestProcessingMixin,
    GroupRequiredMixin,
    WorkeryTemplateView,
    WorkeryListView,
    WorkeryDetailView
)
from tenant_api.filters.partner import PartnerFilter
from tenant_foundation.models import Partner


class PartnerSearchView(LoginRequiredMixin, GroupRequiredMixin, WorkeryTemplateView):
    template_name = 'tenant_partner/search/search_view.html'
    menu_id = "partners"
    group_required = [
        constants.EXECUTIVE_GROUP_ID,
        constants.MANAGEMENT_GROUP_ID,
        constants.FRONTLINE_GROUP_ID
    ]


class PartnerSearchResultView(LoginRequiredMixin, GroupRequiredMixin, WorkeryListView):
    context_object_name = 'partner_list'
    template_name = 'tenant_partner/search/result_view.html'
    paginate_by = 100
    menu_id = "partners"
    skip_parameters_array = ['page']
    group_required = [
        constants.EXECUTIVE_GROUP_ID,
        constants.MANAGEMENT_GROUP_ID,
        constants.FRONTLINE_GROUP_ID
    ]

    def get_queryset(self):
        """
        Override the default queryset to allow dynamic filtering with
        GET parameterss using the 'django-filter' library.
        """
        queryset = None  # The queryset we will be returning.
        keyword = self.request.GET.get('keyword', None)
        if keyword:
            queryset = Partner.objects.full_text_search(keyword)
            queryset = queryset.order_by('last_name', 'given_name')
        else:
            # Remove special characters from the telephone
            tel = self.request.GET.get('telephone')
            tel = tel.replace('(', '')
            tel = tel.replace(')', '')
            tel = tel.replace('-', '')
            tel = tel.replace('+', '')
            tel = tel.replace(' ', '')
            self.request.GET._mutable = True
            self.request.GET['telephone'] = tel

            # Order our results.
            queryset = Partner.objects.all()
            queryset = queryset.order_by('last_name', 'given_name')

            # The following code will use the 'django-filter' library.
            filter = PartnerFilter(self.request.GET, queryset=queryset)
            queryset = filter.qs

        # Attach owners.
        queryset = queryset.prefetch_related('owner')

        return queryset
