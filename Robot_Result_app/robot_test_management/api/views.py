from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from django.db.models import (Count,
                                Max,
                                Min,
                                Q,
                                F,
                                Avg,)
from django.db.models.functions import TruncDay

from core.api.permissions import IsAdmin,IsTeamMemberOfRelatedTeam,IsCommentAuthorOrAdmin

from robot_test_management.models import (TestCase,
                                          TestRun,
                                          TestSuite,
                                          Comment,
                                          Attributes)

from robot_test_management.api.serializers import (CommentSerializer, TestCaseDetaileSerializer, 
                                                   TestRunDetailSerializer, 
                                                   TestRunListSerializer, 
                                                   TestRunSerializer, 
                                                   AttributeSerializer, 
                                                   TestSuiteDetailSerializer)

from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser

from robot_test_management.helpers import db_functions as db

from django_filters.rest_framework import DjangoFilterBackend
from robot_test_management.api.filters import TestRunFilter

from datetime import datetime

class TestRunCreateView(generics.CreateAPIView):
    serializer_class = TestRunSerializer
    parser_classes = [MultiPartParser]

    permission_classes = [IsAuthenticated]


# Testrun Views nonPublic
class TestRunListView(generics.ListAPIView):
    serializer_class = TestRunListSerializer

    permission_classes = [IsAuthenticated,IsTeamMemberOfRelatedTeam]
    
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TestRunFilter
    
    def get_queryset(self):
        team_id = self.kwargs['teampk']
        return TestRun.objects.filter(team_id=team_id)

class TestRunRetreiveView(generics.RetrieveAPIView):
    # TODO: CHANGE THIS TO RETREIVEUPDATEDESTROY VIEW
    serializer_class = TestRunDetailSerializer

    permission_classes = [IsAuthenticated, IsTeamMemberOfRelatedTeam]
    # TODO: Maybe add filtering option to nested suites?

    def get_queryset(self):
        team_id = self.kwargs['teampk']
        return TestRun.objects.filter(team_id=team_id)
    
class TestSuiteReteiveView(generics.RetrieveAPIView):
    serializer_class = TestSuiteDetailSerializer

    permission_classes = [IsAuthenticated, IsTeamMemberOfRelatedTeam]

    def get_queryset(self):
        team_id = self.kwargs['teampk']
        return TestSuite.objects.filter(test_run__team_id=team_id).prefetch_related('test_cases')

class TestCaseRetreiveView(generics.RetrieveAPIView):
    serializer_class = TestCaseDetaileSerializer

    permission_classes = [IsAuthenticated, IsTeamMemberOfRelatedTeam]

    def get_queryset(self):
        team_id = self.kwargs['teampk']
        return TestCase.objects.filter(suite__test_run__team_id=team_id).prefetch_related('keywords')


# Testrun Views Public
class PublicTestRunListView(generics.ListCreateAPIView):
    serializer_class = TestRunListSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TestRun.objects.filter(is_public=True)

class PublicTestRunRetreiveView(generics.RetrieveAPIView):
    serializer_class = TestRunDetailSerializer

    permission_classes = [IsAuthenticated]
    # TODO: Maybe add filtering option to nested suites?

    def get_queryset(self):
        return TestRun.objects.filter(is_public=True)
    
class PublicTestSuiteReteiveView(generics.RetrieveAPIView):
    serializer_class = TestSuiteDetailSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TestSuite.objects.filter(test_run__is_public=True).prefetch_related('test_cases')

class PublicTestCaseRetreiveView(generics.RetrieveAPIView):
    serializer_class = TestCaseDetaileSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TestCase.objects.filter(suite__test_run__is_public=True).prefetch_related('keywords')

# Attribute Views 
class AttributeListView(generics.ListAPIView):
    queryset = Attributes.objects.all()
    serializer_class = AttributeSerializer

    permission_classes=[IsAuthenticated]

class AttributeCreateView(generics.ListCreateAPIView):
    queryset = Attributes.objects.all()
    serializer_class = AttributeSerializer

    permission_classes=[IsAuthenticated, IsAdmin]

    def perform_create(self, serializer):
        key_name = serializer.validated_data['key_name']
        
        TestRun.objects.update(attributes=db.JSONBSet('attributes', key_name, None))
        
        serializer.save()

class AttributeEditView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attributes.objects.all()
    serializer_class = AttributeSerializer

    permission_classes=[IsAuthenticated,IsAdmin]

    def perform_destroy(self, instance):
        key_name = instance.key_name
        TestRun.objects.update(attributes=db.JSONBDeleteKey(key=key_name))
        
        instance.delete()

    def perform_update(self, serializer):
        old_key_name = self.get_object().key_name
        new_key_name = serializer.validated_data['key_name']

        if old_key_name != new_key_name:
            TestRun.objects.filter(attributes__has_key=old_key_name).update(
                attributes=db.JSONBRenameKey(F('attributes'), old_key_name, new_key_name)
            )
            
        serializer.save()

# Comment Views

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsTeamMemberOfRelatedTeam]

    def get_queryset(self):
        testrun_id = self.kwargs['testrunpk']
        return Comment.objects.filter(testrun_id=testrun_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, testrun_id=self.kwargs['testrunpk'])


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsTeamMemberOfRelatedTeam, IsCommentAuthorOrAdmin]


# Dashboard statistics

class TopFailingTestCasesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, teampk):
        failing_testcases = TestCase.objects.filter(
            suite__test_run__team_id=teampk, status="FAIL"
        ).values("name").annotate(
            failure_count=Count('id')
        ).order_by('-failure_count')[:5]
        return Response(failing_testcases)

class DateRangeView(APIView):
    def get(self, request, teampk, format=None):
        date_range = TestRun.objects.filter(team_id=teampk).aggregate(
            min_date=Min('executed_at'),
            max_date=Max('executed_at')
        )
        return Response(date_range, status=status.HTTP_200_OK)

class TreemapDataView(APIView):
    def get(self, request, teampk, format=None):
        start_date = request.query_params.get('start_date')
        suites_aggregated = TestCase.objects.filter(
            suite__test_run__team_id=teampk
        ).values(
            'suite__name'
        ).annotate(
            total_cases=Count('name', distinct=True), 
            failed_cases=Count('id', filter=Q(status='FAIL'))
        )
        if start_date:
            suites_aggregated = suites_aggregated.filter(suite__test_run__executed_at__gte=start_date)

        heatmap_data = [
            {
                'suite_name': suite['suite__name'],
                'total_cases': suite['total_cases'],
                'failed_cases': suite['failed_cases']
            }
            for suite in suites_aggregated
        ]
        return Response(heatmap_data, status=status.HTTP_200_OK)


class TimelineDataView(APIView):
    def get(self, request, teampk, format=None):
        start_date = request.query_params.get('start_date')
        suite_filter = request.query_params.get('suite_filter', '')

        # Query to get the test cases and their failure periods
        test_case_runs = TestCase.objects.filter(
            suite__test_run__team_id=teampk,
            suite__name__icontains=suite_filter,
            status='FAIL'
        ).order_by('name', 'suite__test_run__executed_at').values(
            'name',
            executed_at=F('suite__test_run__executed_at')
        )
        if start_date:
            test_case_runs = test_case_runs.filter(suite__test_run__executed_at__gte=start_date)

        # Group by test case name and create the timeline data
        timeline_data = {}
        for run in test_case_runs:
            test_case_name = run['name']
            if test_case_name not in timeline_data:
                timeline_data[test_case_name] = {
                    'test_case_name': test_case_name,
                    'fail_periods': []
                }

            # Add periods of failure
            if not timeline_data[test_case_name]['fail_periods'] or \
                    timeline_data[test_case_name]['fail_periods'][-1]['end'] != run['executed_at']:
                timeline_data[test_case_name]['fail_periods'].append({
                    'start': run['executed_at'],
                    'end': run['executed_at']
                })
            else:
                # Extend the current failure period
                timeline_data[test_case_name]['fail_periods'][-1]['end'] = run['executed_at']

        # Convert to list and remove test cases with no failures
        timeline_data = [data for data in timeline_data.values() if data['fail_periods']]

        return Response(timeline_data, status=status.HTTP_200_OK)

class TestCaseDurationHeatmapData(APIView):
  def post(self, request, teampk):
        # Retrieve suite name and date from the request data
        suite_name = request.data.get('suite_name')
        date_str = request.data.get('date')  # Expected format: "YYYY-MM"
        
        if not suite_name or not date_str:
            return Response({'error': 'Suite name and date are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Parse the date and calculate the first day of the given month and the first day of the next month
        year, month = map(int, date_str.split('-'))
        first_day_of_month = datetime(year, month, 1)
        if month == 12:
            first_day_of_next_month = datetime(year + 1, 1, 1)
        else:
            first_day_of_next_month = datetime(year, month + 1, 1)
        
        # Filter test cases by the provided team pk, suite name, and date range
        test_cases = TestCase.objects.filter(
            suite__name=suite_name,
            suite__test_run__team__pk=teampk,
            suite__test_run__executed_at__gte=first_day_of_month,
            suite__test_run__executed_at__lt=first_day_of_next_month
        )
        
        # Get the list of unique testcases in the suite
        testcase_names = test_cases.values_list('name', flat=True).distinct()
        
        # Prepare the heatmap data for each testcase
        heatmap_data = []
        for testcase_name in testcase_names:
            # Filter test cases for the specific testcase name
            testcase_runs = test_cases.filter(name=testcase_name)
            
            # Calculate the average duration of the testcase across all runs
            overall_average_duration = testcase_runs.aggregate(Avg('duration'))['duration__avg']
            
            # Aggregate average test case durations by day for the given month
            daily_averages = (
                testcase_runs
                .annotate(day=TruncDay('suite__test_run__executed_at'))
                .values('day')
                .annotate(average_duration=Avg('duration'))
                .order_by('day')
            )
            
            # Append the data to the heatmap_data list
            heatmap_data.append({
                'testcase_name': testcase_name,
                'overall_average_duration': overall_average_duration,
                'daily_averages': list(daily_averages)
            })
        
        return Response(heatmap_data)

# Helper 
class SuiteNames(APIView):
    def get(self, request, teampk):
        return Response(TestSuite.objects.filter(test_run__team_id=teampk).values_list('name', flat=True).distinct(), status=status.HTTP_200_OK)