from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    users_using_invitation = serializers.SerializerMethodField()
    invitations = serializers.StringRelatedField(many=True,)
    invited_by_code = serializers.ReadOnlyField(source="inviter.invite_code",)

    class Meta:
        model = User
        fields = ('phone_number', 'invitation_code', 'activated_invitation_code', 'invited_by_code', 'invitations')
        read_only_fields = ('invitation_code', 'invited_by_code', 'invitations',)


