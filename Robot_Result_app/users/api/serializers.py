from rest_framework import serializers

from users.models import User


class UserDetailSelfSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name','description','avatar')
        read_only_fields = ('avatar',)
        
    def __init__(self, *args, **kwargs):
        super(UserDetailSelfSerializer, self).__init__(*args, **kwargs)

        if self.instance is not None:
            for field_name, field in self.fields.items():
                field.required = False


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','is_staff','is_superuser']


class UserDetailOtherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'description']

