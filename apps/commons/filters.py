import re

from datetime import datetime

from django.db import models
from django.core.exceptions import FieldError
from django.http.response import HttpResponseBadRequest

from rest_framework.filters import BaseFilterBackend


class FieldsQueryFilter(BaseFilterBackend):
    """
    Фильтрация полей
    Использование:
    - *название поля*__*тип фильтра по Django ORM*=*значение*
    """

    @staticmethod
    def get_full_filter_field_name(field_name, prefix='') -> str:
        if prefix:
            return f'{prefix}__{field_name}'
        return field_name

    def get_filter_field_name_with_object_dict(self, model, prefix='') -> dict:
        return {
            self.get_full_filter_field_name(field.name, prefix): field for field in model._meta.get_fields()
        }

    def get_children_filter_fields_with_names(self, parent_model_fields, depth) -> dict:
        children_model_fields = {}

        if depth:
            for parent_model_field_name, parent_model_field in parent_model_fields.items():
                if (
                    isinstance(parent_model_field, models.ForeignKey) or
                    isinstance(parent_model_field, models.ManyToManyField)
                ):
                    model = parent_model_field.remote_field.model
                    children_model_fields.update(self.get_filter_fields_with_names(
                        model, depth - 1, prefix=parent_model_field_name
                    ))
                                    
        return children_model_fields
    
    def get_filter_fields_with_names(self, model, depth=0, prefix='') -> dict:
        parent_model_fields = self.get_filter_field_name_with_object_dict(model, prefix)
        children_model_fields = self.get_children_filter_fields_with_names(
            parent_model_fields, depth
        )

        return {**parent_model_fields, **children_model_fields}

    @staticmethod
    def get_depth_of_filters(items):
        return max([item.count('__') for item in list(items.keys())])

    @staticmethod
    def get_request_params_with_values(request) -> list:
        return list(map(lambda k: (k[0], k[1]), request.GET.items()))

    @staticmethod
    def get_sorted_fields_names(fields_names) -> list:
        fields_names.sort(
            key=lambda field_name: (field_name.count('__'), len(field_name)), 
            reverse=True
        )

        return fields_names
    
    @staticmethod
    def get_separate_field_name_and_filter_type(param, fields_names):
        for field_name in fields_names:
            if field_name in param:
                if field_name == param:
                    return field_name, None
                return field_name, param[len(field_name) + 2:]

        return None, None

    @staticmethod
    def get_filters_dict(filter_field_name, value, filter_type=None) -> dict:
        if not filter_type:
            return {filter_field_name: value}
        return {f"{filter_field_name}__{filter_type}": value}

    @staticmethod
    def add_filter_type(filter_type_base, filter_type_new) -> str:
        if filter_type_base:
            filter_type_base += '__'
        return filter_type_base + filter_type_new

    @staticmethod
    def rebase_filter_type(filter_type_base, filter_type_new) -> str:
        if filter_type_base:
            filter_type_base = '__' + filter_type_base
        return filter_type_new + filter_type_base

    def filter_by_field_name(self, queryset, field_name, value, field_items, filter_type=None):
        field = field_items.get(field_name)

        # для запросов без parameter=STRING (LIKE без учета регистра)
        if (
            isinstance(field, models.CharField) and
            not filter_type and
            not field_name.split('__')[-1] in ('key', 'code')
        ):
            filter_type = 'icontains'

        if (isinstance(field, models.DateTimeField) and
                filter_type in ('', 'lt', 'gt') and
                datetime.strptime(value, '%Y-%m-%d')):
            filter_type = self.rebase_filter_type(filter_type, 'date')
        
        if filter_type == 'in':
            value = value.split(',')
        
        # try:
        if isinstance(field, models.JSONField):
            p = re.compile('(-)?\d+(\.\d+)?')

            if p.match(value):
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
            elif value == 'True':
                value = True
            elif value == 'False':
                value = False
        
        print(type(value))

        return queryset.filter(**self.get_filters_dict(
            field_name, value, filter_type
        ))
        # except (ValueError, FieldError):
        #     # TODO: добавить в readme известные функции фильтрации
        #     raise HttpResponseBadRequest(
        #         'Параметр недействителен. Используйте известные функции фильтрации'
        #     )

    def filter_queryset(self, request, queryset, view=None):
        request_items = self.get_request_params_with_values(request)

        if request_items:
            field_items = self.get_filter_fields_with_names(
                queryset.model, depth=self.get_depth_of_filters(dict(request_items))
            )
            fields_names = self.get_sorted_fields_names(list(field_items.keys()))

            for param, value in request_items:
                print('d', param, value)
                field_name, filter_type = self.get_separate_field_name_and_filter_type(
                    param, fields_names
                )

                if field_name:
                    queryset = self.filter_by_field_name(
                        queryset, field_name, value, field_items, filter_type
                    )

        return queryset
