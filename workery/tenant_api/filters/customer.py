# -*- coding: utf-8 -*-
import django_filters
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Q
from tenant_foundation.models import Customer, Organization
from django.db import models


class CustomerFilter(django_filters.FilterSet):
    o = django_filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('id', 'id'),
            ('given_name', 'given_name'),
            ('last_name', 'last_name'),
            ('telephone', 'telephone'),
            ('email', 'email'),
            ('join_date', 'join_date'),
        ),

        # # labels do not need to retain order
        # field_labels={
        #     'username': 'User account',
        # }
    )

    def keyword_filtering(self, queryset, name, value):
        return Customer.objects.partial_text_search(value)

    search = django_filters.CharFilter(method='keyword_filtering')

    def email_filtering(self, queryset, name, value):
        # DEVELOPERS NOTE:
        # `Django REST Framework` appears to replace the plus character ("+")
        # with a whitespace, as a result, to fix this issue, we will replace
        # the whitespace with the plus character for the email.
        value = value.replace(" ", "+")

        # Search inside user account OR the customer account, then return
        # our filtered results.
        queryset = queryset.filter(
            Q(owner__email=value)|
            Q(email=value)
        )
        return queryset

    email = django_filters.CharFilter(method='email_filtering')

    def telephonel_filtering(self, queryset, name, value):
        return queryset.filter(Q(telephone=value)|Q(other_telephone=value))

    telephone = django_filters.CharFilter(method='telephonel_filtering')

    def organization_name_filtering(self, queryset, name, value):
        organization_pks = Organization.objects.filter(
            Q(name__icontains=value) |
            Q(name__istartswith=value) |
            Q(name__iendswith=value) |
            Q(name__exact=value) |
            Q(name__icontains=value)
        ).values_list("id", flat=True)
        return queryset.filter(organization__id__in=organization_pks)

    organization_name = django_filters.CharFilter(method='organization_name_filtering')

    class Meta:
        model = Customer
        fields = [
            # 'organizations',
            'search',
            'given_name',
            'middle_name',
            'last_name',
            'street_address',
            'telephone',
            'email',
            # # 'business',
            # # 'birthdate',
            # # 'join_date',
            # # 'hourly_salary_desired',
            # # 'limit_special',
            # # 'dues_date',
            # # 'commercial_insurance_expiry_date',
            # # 'police_check',
            # # 'drivers_license_class',
            # # 'how_hear',
            # # 'skill_sets',
            # # 'created_by',
            # # 'last_modified_by',
            # # 'comments',
            'owner__email',
            'telephone',
            'organization_name',
            'state',
        ]
        filter_overrides = {
            models.CharField: { # given_name
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.CharField: { # given_name
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.CharField: { # middle_name
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.CharField: { # last_name
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.CharField: { # street_address
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.CharField: { # owner__email
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            # DEVELOPERS NOTE:
            # - We need custom overrides for the "django_filters" library to
            #   work with the "django-phonenumber-field".
            PhoneNumberField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            }
        }
