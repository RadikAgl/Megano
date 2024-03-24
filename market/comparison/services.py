from comparison.models import Comparison


def add_to_comparison_service(request, user, product_id):
    comparison, created = Comparison.objects.get_or_create(user=user)
    if created:
        pass
    if product_id not in comparison.products.all():
        comparison.products.add(product_id)
        return True  # Return True if the product was added successfully
    return False  # Return False if the product was already in the comparison list


def remove_from_comparison(user, product_id):
    comparison, created = Comparison.objects.get_or_create(user=user)
    if product_id in comparison.products.all():
        comparison.products.remove(product_id)
        return True  # Return True if the product was removed successfully
    return False  # Return False if the product was not in the comparison list


def get_comparison_list(user_id):
    try:
        # Try to retrieve the comparison object associated with the user
        comparison = Comparison.objects.get(user_id=user_id)
        # Return all products related to the retrieved comparison
        return comparison.products.all()
    except Comparison.DoesNotExist:
        # If no comparison exists for the user, return an empty list
        return []


def get_comparison_count(user):
    comparison, created = Comparison.objects.get_or_create(user=user)
    return comparison.products.count()


class ComparisonService:
    def __init__(self):
        self.comparison_model = Comparison
