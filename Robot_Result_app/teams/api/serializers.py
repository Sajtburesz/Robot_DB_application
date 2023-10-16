from rest_framework import serializers
from teams.models import Team,TeamMembership
from django.contrib.auth import get_user_model


class TeamMemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    role = serializers.SerializerMethodField()

    class Meta:
        model = TeamMembership
        fields = ['username', 'role']

    def get_role(self, obj):
        if obj.user == obj.team.owner:
            return "Owner"
        elif obj.is_maintainer:
            return "Maintainer"
        else:
            return "Member"

class TeamSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    owner = serializers.SlugRelatedField(slug_field='username', read_only=True)
    members = TeamMemberSerializer(source='teammembership_set', many=True, read_only=True)
    is_maintainer = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'name', 'owner', 'members', 'is_maintainer']

    def get_is_maintainer(self, obj):
        try:
            user = self.context['request'].user
            membership = TeamMembership.objects.get(user=user, team=obj)
            return membership.is_maintainer
        except TeamMembership.DoesNotExist:
            return False

    def create(self, validated_data):
        # Set the request maker as the team's owner
        owner = self.context['request'].user
        validated_data['owner'] = owner
        team = Team.objects.create(**validated_data)
        
        # Add the owner to the team's members
        TeamMembership.objects.create(team=team, user=owner)
        
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
                TeamMembership.objects.create(team=instance, user=user)
        
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
                TeamMembership.objects.filter(team=instance, user=user).delete()
    
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
    

class RoleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)

    class Meta:
        model = TeamMembership
        fields = ['username', 'is_maintainer']


