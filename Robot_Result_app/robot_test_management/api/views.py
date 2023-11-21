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

from robot_test_management.api.serializers import (CommentSerializer, 
                                                   CommentUpdateSerializer, 
                                                   TestCaseDetaileSerializer, 
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
    
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TestRunFilter
    
    def get_queryset(self):        
        team_id = self.kwargs.get('teamId')
        if team_id == "public":
            return TestRun.objects.filter(is_public=True).order_by('-executed_at')
        elif team_id is not None:
            try:
                return TestRun.objects.filter(team_id=team_id).order_by('-executed_at')
            except ValueError:
                return Response({"detail": "Team Id has to be integer or str public."}, status=status.HTTP_400_BAD_REQUEST)
        

    def get_permissions(self):
        team_id = self.kwargs.get('teamId')

        if team_id == "public":
            return [IsAuthenticated()]
        else:
            return [IsAuthenticated(),IsTeamMemberOfRelatedTeam()]

class TestRunRetreiveView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TestRunDetailSerializer
    permission_classes = [IsAuthenticated,IsTeamMemberOfRelatedTeam]
    # TODO: Maybe add filtering option to nested suites?

    def get_queryset(self):
        team_id = self.kwargs.get('teamId')
        return TestRun.objects.filter(team_id=team_id)


class TestRunRetreivePublicView(generics.RetrieveAPIView):
    serializer_class = TestRunDetailSerializer
    permission_classes = [IsAuthenticated]
    # TODO: Maybe add filtering option to nested suites?

    def get_queryset(self):
        return TestRun.objects.filter(is_public = True)


class TestSuiteReteiveView(generics.RetrieveAPIView):
    serializer_class = TestSuiteDetailSerializer

    def get_queryset(self):
        team_id = self.kwargs.get('teamId')

        if team_id == "public":
            return TestSuite.objects.filter(test_run__is_public=True).prefetch_related('test_cases')
        else:
            try:
                return TestSuite.objects.filter(test_run__team_id=team_id).prefetch_related('test_cases')
            except ValueError:
                return Response({"detail": "Team Id has to be integer or str public."}, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        team_id = self.kwargs.get('teamId')

        if team_id == "public":
            return [IsAuthenticated()]
        else:
            return [IsAuthenticated(),IsTeamMemberOfRelatedTeam()]

class TestCaseRetreiveView(generics.RetrieveAPIView):
    serializer_class = TestCaseDetaileSerializer

    def get_queryset(self):
        team_id = self.kwargs.get('teamId')

        if team_id == "public":
            return TestCase.objects.filter(suite__test_run__is_public=True).prefetch_related('keywords')
        else:
            try:
                return TestCase.objects.filter(suite__test_run__team_id=team_id).prefetch_related('keywords')
            except ValueError:
                return Response({"detail": "Team Id has to be integer or str public."}, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        team_id = self.kwargs.get('teamId')

        if team_id == "public":
            return [IsAuthenticated()]
        else:
            return [IsAuthenticated(),IsTeamMemberOfRelatedTeam()]


# Attribute Views 
class AttributeListView(generics.ListAPIView):
    queryset = Attributes.objects.all().order_by('key_name')
    serializer_class = AttributeSerializer

    permission_classes=[IsAuthenticated]

class AttributeCreateView(generics.ListCreateAPIView):
    queryset = Attributes.objects.all().order_by('key_name')
    serializer_class = AttributeSerializer

    permission_classes=[IsAuthenticated, IsAdmin]

    def perform_create(self, serializer):
        key_name = serializer.validated_data['key_name']
        
        TestRun.objects.update(attributes=db.JSONBSet('attributes', key_name, None))
        
        serializer.save()

class AttributeEditView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attributes.objects.all().order_by('key_name')
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
        testrun_id = self.kwargs.get('testrunpk')
        return Comment.objects.filter(testrun_id=testrun_id).order_by('created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, testrun_id=self.kwargs.get('testrunpk'))


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentUpdateSerializer
    permission_classes = [IsAuthenticated, IsTeamMemberOfRelatedTeam, IsCommentAuthorOrAdmin]

    def get_queryset(self):
        comment_id = self.kwargs.get('pk')
        return Comment.objects.filter(id = comment_id)

# Dashboard statistics

class TopFailingTestCasesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, teamId):

        if teamId == "public":
            failing_testcases = TestCase.objects.filter(
                suite__test_run__is_public=True, status="FAIL"
            ).values("name").annotate(
                failure_count=Count('id')
            ).order_by('-failure_count')[:5]

            return Response(failing_testcases)
        else:
            try:
                failing_testcases = TestCase.objects.filter(
                    suite__test_run__team_id=teamId, status="FAIL"
                ).values("name").annotate(
                    failure_count=Count('id')
                ).order_by('-failure_count')[:5]

                return Response(failing_testcases)
            except ValueError:
                return Response({"detail": "Team Id has to be integer or str public."}, status=status.HTTP_400_BAD_REQUEST)
            


class DateRangeView(APIView):
    def get(self, request, teamId, format=None):
    
        if teamId == "public":
                date_range = TestRun.objects.filter(is_public=True).aggregate(
                    min_date=Min('executed_at'),
                    max_date=Max('executed_at')
                )
                
                return Response(date_range, status=status.HTTP_200_OK)
        else:
            try:
                date_range = TestRun.objects.filter(team_id=teamId).aggregate(
                    min_date=Min('executed_at'),
                    max_date=Max('executed_at')
                )

                return Response(date_range, status=status.HTTP_200_OK)
            except ValueError:
                return Response({"detail": "Team Id has to be integer or str public."}, status=status.HTTP_400_BAD_REQUEST)
            

class TreemapDataView(APIView):
    def get(self, request, teamId, format=None):
           
        start_date = request.query_params.get('start_date')
        if teamId == "public":
                suites_aggregated = TestCase.objects.filter(
                    suite__test_run__is_public=True
                ).values(
                    'suite__name'
                ).annotate(
                    total_cases=Count('name', distinct=True), 
                    failed_cases=Count('id', filter=Q(status='FAIL'))
                )
        else:
            try:
                suites_aggregated = TestCase.objects.filter(
                    suite__test_run__team_id=teamId
                ).values(
                    'suite__name'
                ).annotate(
                    total_cases=Count('name', distinct=True), 
                    failed_cases=Count('id', filter=Q(status='FAIL'))
                )
            except ValueError:
                return Response({"detail": "Team Id has to be integer or str public."}, status=status.HTTP_400_BAD_REQUEST)

        if start_date:
            suites_aggregated = suites_aggregated.filter(suite__test_run__executed_at__gte=start_date)

        treemap_data = [
            {
                'suite_name': suite['suite__name'],
                'total_cases': suite['total_cases'],
                'failed_cases': suite['failed_cases']
            }
            for suite in suites_aggregated
        ]
        return Response(treemap_data, status=status.HTTP_200_OK)

class TimelineDataView(APIView):
    def get(self, request, teamId, format=None):
        start_date = request.query_params.get('start_date')
        suite_filter = request.query_params.get('suite_filter', '')

        # Query to get the test cases and their failure periods
        if teamId == "public":
                test_case_runs = TestCase.objects.filter(
                    suite__test_run__is_public=True,
                    suite__name__icontains=suite_filter,
                    status='FAIL'
                ).order_by('name', 'suite__test_run__executed_at').values(
                    'name',
                    executed_at=F('suite__test_run__executed_at')
                )
        else:
            try:
                test_case_runs = TestCase.objects.filter(
                    suite__test_run__team_id=teamId,
                    suite__name__icontains=suite_filter,
                    status='FAIL'
                ).order_by('name', 'suite__test_run__executed_at').values(
                    'name',
                    executed_at=F('suite__test_run__executed_at')
                )
            except ValueError:
                return Response({"detail": "Team Id has to be integer or str public."}, status=status.HTTP_400_BAD_REQUEST)


        if start_date:
            test_case_runs = test_case_runs.filter(suite__test_run__executed_at__gte=start_date)

        # Group by test case name and create the timeline data
        timeline_data = {}
        for run in test_case_runs:
            test_case_name = run['name']
            executed_at = run['executed_at']

            # Check if this is the first time we see this test case fail
            if test_case_name not in timeline_data:
                timeline_data[test_case_name] = {
                    'test_case_name': test_case_name,
                    'fail_periods': [{
                        'start': executed_at,
                        'end': executed_at
                    }]
                }
            else:
                # Get the last period of failure for the test case
                last_period = timeline_data[test_case_name]['fail_periods'][-1]
                last_fail_date = last_period['end'].date()

                # Check if the current failure is consecutive (next day) to the last failure
                if (executed_at.date() - last_fail_date).days == 1:
                    # It is a consecutive failure, extend the end of the last period
                    last_period['end'] = executed_at
                elif (executed_at.date() - last_fail_date).days > 1:
                    # There was at least a day without failures, start a new period
                    timeline_data[test_case_name]['fail_periods'].append({
                        'start': executed_at,
                        'end': executed_at
                    })

        # Convert to list and remove test cases with no failures
        timeline_data = [data for data in timeline_data.values() if data['fail_periods']]

        return Response(timeline_data, status=status.HTTP_200_OK)

class TestCaseDurationHeatmapData(APIView):
  def post(self, request, teamId):
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
        if teamId == "public":
            test_cases = TestCase.objects.filter(
                suite__name=suite_name,
                suite__test_run__is_public=True,
                suite__test_run__executed_at__gte=first_day_of_month,
                suite__test_run__executed_at__lt=first_day_of_next_month
            )
        else:
            try:
                test_cases = TestCase.objects.filter(
                    suite__name=suite_name,
                    suite__test_run__team__pk=teamId,
                    suite__test_run__executed_at__gte=first_day_of_month,
                    suite__test_run__executed_at__lt=first_day_of_next_month
                )
            except ValueError:
                return Response({"detail": "Team Id has to be integer or str public."}, status=status.HTTP_400_BAD_REQUEST)

        
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
    def get(self, request, teamId):
        if teamId == 'public':
            return Response(TestSuite.objects.filter(test_run__is_public=True).values_list('name', flat=True).distinct(), status=status.HTTP_200_OK)
        else:
            try:
                return Response(TestSuite.objects.filter(test_run__team_id=teamId).values_list('name', flat=True).distinct(), status=status.HTTP_200_OK)
            except ValueError:
                return Response({"detail": "Team Id has to be integer or str public."}, status=status.HTTP_400_BAD_REQUEST)   