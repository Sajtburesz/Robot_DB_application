from rest_framework import serializers
from teams.models import Team
from django.contrib.auth import get_user_model


class TeamSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    owner = serializers.SlugRelatedField(slug_field='username', read_only=True)
    members = serializers.SlugRelatedField(slug_field='username', read_only=True, many=True)
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'owner', 'members']

    def create(self, validated_data):
        # Set the request maker as the team's owner
        owner = self.context['request'].user
        validated_data['owner'] = owner
        team = Team.objects.create(**validated_data)
        
        # Add the owner to the team's members
        team.members.add(owner)
        
        return team

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

class AddMembersSerializer(serializers.ModelSerializer):
    members = serializers.SlugRelatedField(
        slug_field='username',
        queryset=get_user_model().objects.all(),
        many=True
    )

    class Meta:
        model = Team
        fields = ['members']

    def update(self, instance, validated_data):
        members = validated_data.get('members', [])

        for user in members:
            if user not in instance.members.all():
                instance.members.add(user)
        
        return instance
    
class RemoveMembersSerializer(serializers.ModelSerializer):
    members = serializers.SlugRelatedField(
        slug_field='username',
        queryset=get_user_model().objects.all(),
        many=True
    )

    class Meta:
        model = Team
        fields = ['members']

    def update(self, instance, validated_data):
        members = validated_data.get('members', [])

        for user in members:
            if user == instance.owner:
                raise serializers.ValidationError(f"Owner {instance.owner} can't be removed from team.")
            if user in instance.members.all():
                instance.members.remove(user)
    
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
    



