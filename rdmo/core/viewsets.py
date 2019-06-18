from django.conf import settings
from django.contrib.sites.models import Site

from rest_framework import viewsets
from rest_framework.response import Response

from rdmo.core.permissions import HasModelPermission

from .serializers import SiteSerializer


class SettingsViewSet(viewsets.GenericViewSet):

    def list(self, request, *args, **kwargs):
        return Response({
            'default_uri_prefix': settings.DEFAULT_URI_PREFIX
        })


class SitesViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
