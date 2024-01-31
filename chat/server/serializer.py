from rest_framework import serializers

# internal
from .models import Server, Channel


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'


class ServerSerializer(serializers.ModelSerializer):

    num_members = serializers.SerializerMethodField()
    channel_server = ChannelSerializer(many=True)

    class Meta:
        model = Server
        exclude = ("member",)

    def get_num_members(self, obj):
        """
        Custom method to retrieve the number of members for a server instance.

        Args:
        - obj: The Server instance.

        Returns:
        - The number of members in the server, or None if not available.
        """
        if hasattr(obj, 'num_members'):
            return obj.num_members
        return None

    def to_representation(self, instance):
        """
        Custom method to customize the serialized representation by conditionally removing 'num_members'.

        Args:
        - instance: The Server instance being serialized.

        Returns:
        - The serialized representation with 'num_members' removed if not present in the context.
        """
        data = super().to_representation(instance)
        num_members = self.context.get('num_members')
        if not num_members:
            data.pop('num_members', None)
        return data
