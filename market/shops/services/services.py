from shops.models import Shop


def create_shop(user, data):
    """
    Create a shop for the given user with the provided data.
    """
    shop = Shop.objects.create(user=user, **data)
    return shop


def remove_shop(shop):
    """
    Remove the provided shop.
    """
    shop.delete()
