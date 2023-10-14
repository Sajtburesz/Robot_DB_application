from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from robot_test_management.models import TestCase,TestRun,TestSuite,Keyword
from robot_test_management.helpers.robot_parser import parse_robot_output

import random

class UploadRobotOutputView(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request):
        # Extract file from the request
        file_obj = request.data['file']
        
        # Parse the Robot Framework's XML output
        parsed_data = parse_robot_output(file_obj)

        # Lists to hold instances for batch creation
        suites_to_create = []
        tests_to_create = []
        keywords_to_create = []

        # Process parsed data
        for suite_data in parsed_data:
            # test_run = TestRun(attributes={})  # Assuming no specific attributes for now
            rand = random.randint()
            test_run = TestRun(name=f"test-run{rand}")
            test_run.save()  # We need to save this immediately to get an ID for foreign key relations

            test_suite = TestSuite(name=suite_data['name'], test_run=test_run)
            suites_to_create.append(test_suite)
            
            for test_data in suite_data['tests']:
                test_case = TestCase(name=test_data['name'], status=test_data['status'], suite=test_suite)
                tests_to_create.append(test_case)
                
                for keyword_data in test_data['keywords']:
                    keyword = Keyword(
                        name=keyword_data['name'],
                        status=keyword_data['status'],
                        log_message=keyword_data.get('log_message', None),
                        test_case=test_case
                    )
                    keywords_to_create.append(keyword)

        # Batch create instances
        TestSuite.objects.bulk_create(suites_to_create)
        TestCase.objects.bulk_create(tests_to_create)
        Keyword.objects.bulk_create(keywords_to_create)
        
        # Return a success response
        return Response({"message": "File processed successfully!"}, status=status.HTTP_201_CREATED)
