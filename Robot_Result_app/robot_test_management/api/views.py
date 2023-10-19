from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from robot_test_management.models import TestCase,TestRun,TestSuite,Keyword,Attributes
from robot_test_management.api.serializers import TestRunSerializer, AttributeSerializer, TestRunUploadSerializer
from robot_test_management.helpers.robot_parser import parse_robot_output
from rest_framework.permissions import IsAuthenticated

from django.db.models import F, Func, Value


class TestRunUploadView(generics.CreateAPIView):
    serializer_class = TestRunUploadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Parse the XML
        output_xml = request.data['output_xml']
        parsed_data = parse_robot_output(output_xml)

        # Insert into the database
        test_run = TestRun.objects.create(version=request.data['version'])

        
        # Lists to gather objects
        test_suites_to_create = []
        test_cases_to_create = []
        keywords_to_create = []


        for suite_data in parsed_data:
            if suite_data is None:
                continue
            test_suite = TestSuite(name=suite_data['name'], test_run=test_run)
            test_suites_to_create.append(test_suite)

            for test_data in suite_data['tests']:
                test_case = TestCase(name=test_data['name'], status=test_data['status'], suite=test_suite)
                test_cases_to_create.append(test_case)
                
                for keyword_data in test_data['keywords']:
                    keyword = Keyword(name=keyword_data['name'], status=keyword_data['status'], test_case=test_case)
                    keywords_to_create.append(keyword)

        # Use bulk_create to create the objects in the database
        TestSuite.objects.bulk_create(test_suites_to_create)
        TestCase.objects.bulk_create(test_cases_to_create)
        Keyword.objects.bulk_create(keywords_to_create)

        return Response({"message": "TestRun uploaded and parsed successfully."}, status=status.HTTP_201_CREATED)

class TestRunListView(generics.ListAPIView):
    queryset = TestRun.objects.all()
    serializer_class = TestRun


class JSONBDeleteKey(Func):
    function = '#-'
    template = '"attributes" #- ARRAY[%(key)s]'
    
    def __init__(self, key, **extra):
        key_as_array = '\'{}\''.format(key)  
        super(JSONBDeleteKey, self).__init__(key=key_as_array, **extra)

class JSONBRenameKey(Func):
    function = 'jsonb_set'
    template = "%(function)s(%(expressions)s - '%(old_key)s', '{%(new_key)s}', %(expressions)s->'%(old_key)s')"

    def __init__(self, expression, old_key, new_key, **extra):
        super(JSONBRenameKey, self).__init__(expression, old_key=old_key, new_key=new_key, **extra)


class JSONBSet(Func):
    function = 'jsonb_set'
    template = "%(function)s(%(expressions)s, '{\"%(key_name)s\"}', '\"%(default_value)s\"', true)"

    def __init__(self, expression, key_name, default_value, **extra):
        super(JSONBSet, self).__init__(expression, key_name=str(key_name), default_value=str(default_value), **extra)

class AttributeListView(generics.ListCreateAPIView):
    queryset = Attributes.objects.all()
    serializer_class = AttributeSerializer

    def perform_create(self, serializer):
        key_name = serializer.validated_data['key_name']
        
        # Efficiently add the new attribute key with a default value to all TestRun instances at the database level
        TestRun.objects.update(attributes=JSONBSet('attributes', key_name, None))
        
        serializer.save()

class AttributeEditView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attributes.objects.all()
    serializer_class = AttributeSerializer

    def perform_destroy(self, instance):
        key_name = instance.key_name
        # Efficiently update all TestRun instances to remove the key from their attributes JSONField.
        TestRun.objects.update(attributes=JSONBDeleteKey(key=key_name))
        
        instance.delete()

    def perform_update(self, serializer):
        old_key_name = self.get_object().key_name
        new_key_name = serializer.validated_data['key_name']

        # If the key name has changed, we should update all TestRun instances.
        if old_key_name != new_key_name:
            # Efficiently rename the attribute key for all TestRun instances at the database level
            TestRun.objects.filter(attributes__has_key=old_key_name).update(
                attributes=JSONBRenameKey(F('attributes'), old_key_name, new_key_name)
            )
            
        serializer.save()