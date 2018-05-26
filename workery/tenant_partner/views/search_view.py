# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic import DetailView, ListView, TemplateView
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from shared_foundation.mixins import ExtraRequestProcessingMixin
from tenant_api.filters.partner import PartnerFilter
from tenant_foundation.models import Partner


class PartnerSearchView(LoginRequiredMixin, TemplateView):
    template_name = 'tenant_partner/search/search_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = "partners"
        return context


class PartnerSearchResultView(LoginRequiredMixin, ListView, ExtraRequestProcessingMixin):
    context_object_name = 'partner_list'
    queryset = Partner.objects.order_by('-created')
    template_name = 'tenant_partner/search/result_view.html'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        modified_context = super().get_context_data(**kwargs)

        # Required for navigation
        modified_context['current_page'] = "partners"

        # DEVELOPERS NOTE:
        # - This class based view will have URL parameters for filtering and
        #   searching records.
        # - We will extract the URL parameters and save them into our context
        #   so we can use this to help the pagination.
        modified_context['filter_parameters'] = self.get_param_urls(['page'])

        # Return our modified context.
        return modified_context

    def get_queryset(self):
        """
        Override the default queryset to allow dynamic filtering with
        GET parameterss using the 'django-filter' library.
        """
        queryset = None  # The queryset we will be returning.
        keyword = self.request.GET.get('keyword', None)
        if keyword:
            queryset = Partner.objects.full_text_search(keyword)
            queryset = queryset.order_by('-created')
        else:
            queryset = super(PartnerListView, self).get_queryset()

        # The following code will use the 'django-filter'
        filter = PartnerFilter(self.request.GET, queryset=queryset)
        queryset = filter.qs
        queryset = queryset.prefetch_related(
            'owner',
        )
        return queryset
