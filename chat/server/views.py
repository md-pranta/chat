# Import necessary modules
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response

# Import internal modules
from .models import Server
from .schema import server_list_docs
from .serializer import ServerSerializer

# Define views for the Server model


class ServerListViewSet(viewsets.ViewSet):
    # Set the queryset to include all Server objects
    queryset = Server.objects.all()

    # Define the list view for the Server model
    @server_list_docs
    def list(self, request):
        # Extract query parameters from the request
        category = request.query_params.get('category')
        qty = request.query_params.get('qty')
        by_user = request.query_params.get('by_user') == 'true'
        with_num_members = request.query_params.get(
            'with_num_members') == 'true'
        by_serverID = request.query_params.get('by_serverID')

        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if by_user:
            if request.user.is_authenticated:
                user_id = request.user.id
                self.queryset = self.queryset.filter(member=user_id)
            else:
                raise AuthenticationFailed()
        # Annotate queryset with the number of members if 'with_num_members' is true
        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count('member'))

        if qty:
            self.queryset = self.queryset[: int(qty)]
        # Filter queryset based on the 'by_serverID' parameter
        if by_serverID:
            if not request.user.is_authenticated:
                raise AuthenticationFailed()
            try:
                self.queryset = self.queryset.filter(id=by_serverID)
                if not self.queryset.exists():
                    raise ValidationError(
                        detail=f'sever with id {by_serverID} not found')
            except ValueError:
                raise ValidationError(detail='server value error')
        # Serialize the queryset using ServerSerializer
        serializer = ServerSerializer(
            self.queryset, many=True, context={'num_members': with_num_members})
        # Return the serialized data as a response
        return Response(serializer.data)
