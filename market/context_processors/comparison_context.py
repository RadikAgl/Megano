from comparison.views import ComparisonView


def comparison_count(request):
    """Количество сравнений."""
    comparison_count_value = ComparisonView.comparison_count(request)
    return {"comparison_count": comparison_count_value}
