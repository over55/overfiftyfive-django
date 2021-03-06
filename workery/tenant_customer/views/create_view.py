# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, FormView, UpdateView
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
from tenant_api.filters.customer import CustomerFilter
from tenant_foundation.models import (
    Customer,
    SkillSet,
    Tag,
    HowHearAboutUsItem
)


class PickCustomerTypeInCreateView(LoginRequiredMixin, GroupRequiredMixin, WorkeryTemplateView):
    template_name = 'tenant_customer/create/pick_view.html'
    menu_id = "customers"
    group_required = [
        constants.EXECUTIVE_GROUP_ID,
        constants.MANAGEMENT_GROUP_ID,
        constants.FRONTLINE_GROUP_ID
    ]


class ResidentialCustomerCreateView(LoginRequiredMixin, GroupRequiredMixin, WorkeryTemplateView):
    template_name = 'tenant_customer/create/residential_create_view.html'
    menu_id = "customers"
    group_required = [
        constants.EXECUTIVE_GROUP_ID,
        constants.MANAGEMENT_GROUP_ID,
        constants.FRONTLINE_GROUP_ID
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['skill_sets'] = SkillSet.objects.all()
        context['how_hear_set'] = HowHearAboutUsItem.objects.filter(is_for_customer=True).order_by('sort_number')
        return context


class ResidentialCustomerConfirmCreateView(LoginRequiredMixin, GroupRequiredMixin, WorkeryTemplateView):
    template_name = 'tenant_customer/create/residential_confirm_view.html'
    menu_id = "customers"
    group_required = [
        constants.EXECUTIVE_GROUP_ID,
        constants.MANAGEMENT_GROUP_ID,
        constants.FRONTLINE_GROUP_ID
    ]


class CommercialCustomerCreateView(LoginRequiredMixin, GroupRequiredMixin, WorkeryTemplateView):
    template_name = 'tenant_customer/create/commercial_create_view.html'
    menu_id = "customers"
    group_required = [
        constants.EXECUTIVE_GROUP_ID,
        constants.MANAGEMENT_GROUP_ID,
        constants.FRONTLINE_GROUP_ID
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['skill_sets'] = SkillSet.objects.all()
        context['how_hear_set'] = HowHearAboutUsItem.objects.filter(is_for_customer=True).order_by('sort_number')
        return context


class CommercialCustomerConfirmCreateView(LoginRequiredMixin, GroupRequiredMixin, WorkeryTemplateView):
    template_name = 'tenant_customer/create/commercial_confirm_view.html'
    menu_id = "customers"
    group_required = [
        constants.EXECUTIVE_GROUP_ID,
        constants.MANAGEMENT_GROUP_ID,
        constants.FRONTLINE_GROUP_ID
    ]
