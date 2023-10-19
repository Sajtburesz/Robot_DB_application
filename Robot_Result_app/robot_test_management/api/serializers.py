from rest_framework import serializers
from robot_test_management.models import TestCase,TestRun,TestSuite,Keyword,Attributes


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attributes
        fields = '__all__'
    
    def validate(self, data):
        MAX_INSTANCE_COUNT = 6  # Define your maximum limit here
        if Attributes.objects.count() >= MAX_INSTANCE_COUNT:
            raise serializers.ValidationError(f"Maximum allowed instances ({MAX_INSTANCE_COUNT}) of Attributes have been reached.")
        return data

class TestRunUploadSerializer(serializers.Serializer):
    output_xml = serializers.FileField()
    version = serializers.CharField(max_length=40)


class TestRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestRun
        fields = '__all__'
    def validate_attributes(self, attrs):
        all_keys = set(Attributes.objects.values_list('key_name', flat=True))
        
        if attrs:
            extraneous_keys = set(attrs.keys()) - all_keys
            if extraneous_keys:
                raise serializers.ValidationError(f"The following attribute keys are not allowed: {', '.join(extraneous_keys)}")

            # Add any missing keys with a default value of None
            for key in all_keys:
                if key not in attrs:
                    attrs[key] = None
        else:
            # If attributes are not provided, initialize them with all available keys
            attrs = {key: None for key in all_keys}

        return attrs

class TestSuiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestSuite
        fields = '__all__'


class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = '__all__'


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = '__all__'
