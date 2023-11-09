from rest_framework import serializers

from robot_test_management.models import (TestCase,
                                          TestRun,
                                          TestSuite,
                                          Keyword, 
                                          Attributes,
                                          Comment)

from robot_test_management.helpers.robot_parser import parse_robot_output
from django.db import transaction
from django.core.files.uploadedfile import InMemoryUploadedFile

from core.pagination import PageNumberPaginationNoCount


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attributes
        fields = '__all__'
    
    def validate(self, data):
        MAX_INSTANCE_COUNT = 6  # Define your maximum limit here
        if Attributes.objects.count() >= MAX_INSTANCE_COUNT:
            raise serializers.ValidationError(f"Maximum allowed instances ({MAX_INSTANCE_COUNT}) of Attributes have been reached.")
        return data

# Creation of TestRun instance START
class TestRunSerializer(serializers.ModelSerializer):
    output_file = serializers.FileField(write_only=True)
    
    class Meta:
        model = TestRun
        fields = ['output_file', 'attributes', 'team']
    
    
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
    
    def create(self, validated_data):
        
        file_obj = validated_data.pop('output_file')
        
        if isinstance(file_obj, InMemoryUploadedFile):
            # Read the file content directly
            parsed_data, executed_at = parse_robot_output(file_obj)
        else:
            # Use the temporary file path for larger files
            parsed_data, executed_at = parse_robot_output(file_obj.temporary_file_path())

        # Start the transaction block
        with transaction.atomic():
            test_run = TestRun.objects.create(**validated_data, executed_at=executed_at)

            suites_to_create = []
            for suite_data in parsed_data:
                if suite_data is None:
                    continue
                tests_data = suite_data.pop('tests', [])
                suite_instance = TestSuite(test_run=test_run, **suite_data)
                suites_to_create.append((suite_instance, tests_data))

            # Bulk create suites
            created_suites = TestSuite.objects.bulk_create([suite[0] for suite in suites_to_create])

            test_cases_to_create = []
            for idx, (suite, tests_data) in enumerate(suites_to_create):
                for test_data in tests_data:
                    keywords_data = test_data.pop('keywords', [])
                    test_case_instance = TestCase(suite=created_suites[idx], **test_data)
                    test_cases_to_create.append((test_case_instance, keywords_data))

            # Bulk create test cases
            created_test_cases = TestCase.objects.bulk_create([test_case[0] for test_case in test_cases_to_create])

            keywords_to_create = []
            for idx, (test_case, keywords_data) in enumerate(test_cases_to_create):
                for keyword_data in keywords_data:
                    keyword_instance = Keyword(test_case=created_test_cases[idx], **keyword_data)
                    keywords_to_create.append(keyword_instance)

            # Bulk create keywords
            Keyword.objects.bulk_create(keywords_to_create)

        return test_run

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

# Creation of TestRun instance END


# Retreive serializers

class TestRunListSerializer(serializers.ModelSerializer):
    executed_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = TestRun
        fields = ['id', 'attributes', 'team', 'executed_at', 'is_public','status']

    def get_status(self, obj):
        has_failure = TestCase.objects.filter(
            suite__test_run=obj, 
            status='FAIL'
        ).exists()
        return 'FAIL' if has_failure else 'PASS'

# Retreive Single Testrun Instance with Suites

class TestSuiteNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestSuite
        fields = ['id', 'name']
    
# Nested Pagination
class PaginatedTestSuiteSerializer(PageNumberPaginationNoCount):
    def get_paginated_response(self, data):
        return {
            'suites': data,
            'next': self.get_next_link(),
            'previous': self.get_previous_link()
        }


class TestRunDetailSerializer(serializers.ModelSerializer):
    suites = serializers.SerializerMethodField()

    class Meta:
        model = TestRun
        fields = ['id', 'attributes', 'team','suites','executed_at']

    def get_suites(self, obj):
        paginator = PaginatedTestSuiteSerializer()
        paginated_suites = paginator.paginate_queryset(obj.suites.all(), self.context['request'])
        serializer = TestSuiteNameSerializer(paginated_suites, many=True).data
        return paginator.get_paginated_response(serializer)
    

# Retreive TestCases for a suite instance
class TestCaseNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ['id', 'name', 'status']

class TestSuiteDetailSerializer(serializers.ModelSerializer):
    test_cases = TestCaseNameSerializer(many=True, read_only=True)

    class Meta:
        model = TestSuite
        fields = ['id', 'name', 'test_cases']

# Retreive Keywords for FAILED Testcase instances
class KeywordDetaileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = '__all__'

class TestCaseDetaileSerializer(serializers.ModelSerializer):
    keywords = KeywordDetaileSerializer(many=True, read_only=True)

    class Meta:
        model = TestCase
        fields = ['id', 'name','status','duration', 'keywords']

# Comment serializer


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='user.username')  # Display the username

    class Meta:
        model = Comment
        fields = ['id', 'author', 'testrun', 'text', 'created_at', 'updated_at']