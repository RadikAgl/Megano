from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View

from products.models import Product
from .services import ComparisonService, remove_from_comparison, add_to_comparison_service, get_comparison_list


@method_decorator(login_required, name="dispatch")
class ComparisonView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse_lazy("account_login"))

        comparison_list = get_comparison_list(request.user.id)  # Pass user ID to get_comparison_list
        comparison = {"products": comparison_list}  # Assuming this structure matches your template expectations

        return render(request, "comparison/comparison.jinja2", {"comparison": comparison})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse_lazy("account_login"))

        product_id = request.POST.get("product_id")
        action = request.POST.get("action")

        comparison_service = ComparisonService()  # noqa

        if action == "add":
            add_to_comparison(request.user, product_id)
        elif action == "remove":
            remove_from_comparison(request.user, product_id)

        # Get the updated comparison list after adding or removing the product
        comparison_list = get_comparison_list(request.user.id)
        context = {
            "comparison": {"products": comparison_list},
        }
        return render(request, "comparison/comparison.jinja2", context)


@login_required
def add_to_comparison(request, product_id):
    if request.method == "POST":
        # Handle the POST request
        user = request.user  # noqa
        added = add_to_comparison_service(request, request.user, product_id)  # noqa

        # Redirect back to the product detail page
        return HttpResponseRedirect(reverse("products:product-details", args=[product_id]))
    else:
        # Handle the GET request
        # This part is optional, you can render a different template for GET requests if needed
        return HttpResponseNotAllowed(["POST"])


def get_product_details(product_id):
    # Assuming product_id is the primary key of the Product model
    try:
        product = Product.objects.get(pk=product_id)
        details = product.details  # Accessing the details field
        return details
    except Product.DoesNotExist:
        return None
