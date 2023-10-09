from rest_framework import serializers
from teams.models import Team
from django.contrib.auth import get_user_model


class TeamSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required = True)
    owner = serializers.SlugRelatedField(slug_field='username', read_only=True)
    members = serializers.SlugRelatedField(slug_field='username', many=True, read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'owner', 'members']

    def __init__(self, *args, **kwargs):
        super(TeamSerializer, self).__init__(*args, **kwargs)

        if self.context['request'].method in ['PUT', 'PATCH']:
            self.fields['name'].required = False

    def update(self, instance, validated_data):

        members = validated_data.get('members', [])
        for member in instance.members.all():
            if member not in members and member != instance.owner:
                instance.members.remove(member)

        for member in members:
            if member not in instance.members.all():
                instance.members.add(member)


        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

class UserTeamSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    owner_name = serializers.SerializerMethodField()
    class Meta:
        model = Team
        fields = ['id','name','owner_name', 'is_owner']

    def get_is_owner(self, obj):
        user = self.context['request'].user
        return obj.owner == user
    
    def get_owner_name(self,obj):
        return obj.owner.username