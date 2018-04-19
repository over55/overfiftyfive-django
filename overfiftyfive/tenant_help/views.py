# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic import DetailView, ListView, TemplateView
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from shared_foundation.mixins import ExtraRequestProcessingMixin
from tenant_api.filters.staff import StaffFilter
from tenant_foundation.models import (
    Staff,
    SkillSet,
    Tag
)


@method_decorator(login_required, name='dispatch')
class HelpListView(TemplateView):
    template_name = 'tenant_help/list_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = "help" # Required for navigation
        return context
