from products.models import Category


def categories(request):
    all_categories = Category.objects.select_related("parent")

    children = {}

    for category in all_categories:
        children[category.id] = [cat for cat in all_categories if cat.parent_id == category.id]

    return {
        "main_categories": all_categories.filter(parent=None),
        "children": children,
    }
