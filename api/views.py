# netbox/auto_ip_alloc/api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ipam.models import Prefix
from ipam.api.serializers import IPAddressSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType

class AllocateIPView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        prefix_id = request.data.get('prefix_id')
        prefix_str = request.data.get('prefix')

        if not prefix_id and not prefix_str:
            return Response(
                {'error': 'Either "prefix_id" or "prefix" must be provided.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if prefix_id:
                prefix = Prefix.objects.get(pk=prefix_id)
            else:
                prefix = Prefix.objects.get(prefix=prefix_str)
        except Prefix.DoesNotExist:
            return Response({'error': 'Prefix not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Get the next available IP address
        next_ip = prefix.get_first_available_ip()
        if not next_ip:
            return Response(
                {'error': 'No available IPs in this prefix.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Collect optional fields from request data
        optional_fields = [
            'status', 'role', 'description', 'dns_name', 'tenant', 'vrf',
            'custom_fields', 'tags', 'assigned_object_type', 'assigned_object_id'
        ]

        ip_data = {
            'address': str(next_ip) + '/' + str(prefix.prefix.prefixlen),
            'vrf': prefix.vrf.pk if prefix.vrf else None,
            'tenant': prefix.tenant.pk if prefix.tenant else None,
        }

        # Override with any provided fields
        for field in optional_fields:
            value = request.data.get(field)
            if value is not None:
                ip_data[field] = value

        # Handle assigned_object if provided
        assigned_object_type = ip_data.pop('assigned_object_type', None)
        assigned_object_id = ip_data.pop('assigned_object_id', None)
        if assigned_object_type and assigned_object_id:
            try:
                ct = ContentType.objects.get(model=assigned_object_type.split('.')[-1])
                ip_data['assigned_object_type'] = ct.pk
                ip_data['assigned_object_id'] = assigned_object_id
            except ContentType.DoesNotExist:
                return Response(
                    {'error': f'Invalid assigned_object_type: {assigned_object_type}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Use the serializer for validation and creation
        serializer = IPAddressSerializer(data=ip_data, context={'request': request})
        if serializer.is_valid():
            ip_address = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
