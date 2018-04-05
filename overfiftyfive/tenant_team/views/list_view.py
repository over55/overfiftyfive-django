# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic import DetailView, ListView, TemplateView
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from shared_foundation.mixins import ExtraRequestProcessingMixin
from tenant_api.filters.staff import StaffFilter
from tenant_foundation.models import Staff


#---------#
# SUMMARY #
#---------#


@method_decorator(login_required, name='dispatch')
class TeamSummaryView(ListView, ExtraRequestProcessingMixin):
    context_object_name = 'staff_list'
    queryset = Staff.objects.order_by('-created')
    template_name = 'tenant_team/summary/view.html'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        modified_context = super().get_context_data(**kwargs)

        # Required for navigation
        modified_context['current_page'] = "team"

        # DEVELOPERS NOTE:
        # - We will extract the URL parameters and save them into our context
        #   so we can use this to help the pagination.
        modified_context['parameters'] = self.get_params_dict([])

        # Return our modified context.
        return modified_context

    def get_queryset(self):
        queryset = Staff.objects.all()
        queryset = queryset.order_by('-created')
        return queryset


#------#
# LIST #
#------#


@method_decorator(login_required, name='dispatch')
class TeamListView(ListView, ExtraRequestProcessingMixin):
    context_object_name = 'staff_list'
    queryset = Staff.objects.order_by('-created')
    template_name = 'tenant_team/list/view.html'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = "team" # Required for navigation
        return context

    def get_queryset(self):
        queryset = super(TeamListView, self).get_queryset() # Get the base.
        print(queryset)

        # The following code will use the 'django-filter'
        filter = StaffFilter(self.request.GET, queryset=queryset)
        queryset = filter.qs
        return queryset
