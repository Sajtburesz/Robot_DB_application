from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics

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


# Testrun Views
class TestRunCreateView(generics.CreateAPIView):
    serializer_class = TestRunSerializer
    parser_classes = [MultiPartParser]

    permission_classes = [IsAuthenticated]


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