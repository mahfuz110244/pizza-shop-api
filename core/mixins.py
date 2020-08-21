"""
Basic building blocks for generic class based views.

We don't bind behaviour to http method handlers yet,
which allows mixin classes to be composed in interesting ways.
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from core.service import custom_response


class CreateModelMixin:
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return custom_response(success=True, status_code=status.HTTP_201_CREATED, data=serializer.data, headers=headers)
        except Exception as e:
            return custom_response(success=False, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, errorMessage=str(e))

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class ListModelMixin:
    """
    List a queryset.
    """

    def list(self, request, *args, **kwargs):
        # queryset = self.filter_queryset(self.get_queryset())
        #
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        #
        # serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data)
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                data = self.get_paginated_response(serializer.data).data
            else:
                serializer = self.get_serializer(queryset, many=True)
                data = serializer.data
            return custom_response(success=True, status_code=status.HTTP_200_OK, data=data)
        except Exception as e:
            return custom_response(success=False, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, errorMessage=str(e))


class RetrieveModelMixin:
    """
    Retrieve a model instance.
    """

    def retrieve(self, request, *args, **kwargs):
        # instance = self.get_object()
        # serializer = self.get_serializer(instance)
        # return Response(serializer.data)

        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return custom_response(success=True, status_code=status.HTTP_200_OK, data=serializer.data)
        except Exception as e:
            return custom_response(success=False, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                   errorMessage=str(e))



class UpdateModelMixin:
    """
    Update a model instance.
    """

    def update(self, request, *args, **kwargs):
        # partial = kwargs.pop('partial', False)
        # instance = self.get_object()
        # serializer = self.get_serializer(instance, data=request.data, partial=partial)
        # serializer.is_valid(raise_exception=True)
        # self.perform_update(serializer)
        #
        # if getattr(instance, '_prefetched_objects_cache', None):
        #     # If 'prefetch_related' has been applied to a queryset, we need to
        #     # forcibly invalidate the prefetch cache on the instance.
        #     instance._prefetched_objects_cache = {}
        #
        # return Response(serializer.data)

        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            return custom_response(success=True, status_code=status.HTTP_200_OK, data=serializer.data)
        except Exception as e:
            return custom_response(success=False, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                   errorMessage=str(e))

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DestroyModelMixin:
    """
    Destroy a model instance.
    """

    def destroy(self, request, *args, **kwargs):
        # instance = self.get_object()
        # self.perform_destroy(instance)
        # return Response(status=status.HTTP_204_NO_CONTENT)

        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return custom_response(success=True, status_code=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return custom_response(success=False, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                   errorMessage=str(e))

    def perform_destroy(self, instance):
        instance.delete()
