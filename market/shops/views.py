from django.shortcuts import render, get_object_or_404
from .models import Seller


def seller_detail(request, seller_id):
    """Функция отображает  страницу с детальной информацией о продавце"""

    seller = get_object_or_404(Seller, pk=seller_id)
    return render(request, "seller_detail.html", {"seller": seller})
