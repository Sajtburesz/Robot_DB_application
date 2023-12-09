import django_filters

from robot_test_management.models import TestRun, TestSuite

class TestRunFilter(django_filters.FilterSet):
    class Meta:
        model = TestRun
        fields = []

    def filter_queryset(self, queryset):

        queryset = super().filter_queryset(queryset)

        for key, value in self.request.GET.items():
            if key == 'executed_at':
                queryset = queryset.filter(executed_at__date__icontains=value)
            if key not in ["page"]:
                key_exact_lookup = f'attributes__has_key'
                value_icontains_lookup = f'attributes__{key}__icontains'

                if queryset.filter(**{key_exact_lookup: key}).exists():
                    queryset = queryset.filter(**{value_icontains_lookup: value})
        
        return queryset
    
class SuiteFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = TestSuite
        fields = ['name']