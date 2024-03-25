from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormView

from accounts.models import User
from cart.models import Cart, ProductInCart
from comparison.services import get_comparison_list
from .forms import FirstStepForm, SecondStepForm, ThirdStepForm
from .models import Order


class FirstOrderView(LoginRequiredMixin, FormView):
    form_class = FirstStepForm

    template_name = "order/order.jinja2"
    success_url = reverse_lazy("url:step2")

    def form_valid(self, form):
        self.request.session[self.request.user.id] = {}
        self.request.session[self.request.user.id] = {
            "name": form.cleaned_data["name"],
            "phone": form.cleaned_data["phone"],
        }

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "не верный ввод полей")
        return super().form_invalid(form)


class SecondOrderView(LoginRequiredMixin, FormView):
    template_name = "order/order_2.jinja2"
    success_url = reverse_lazy("url:step3")
    form_class = SecondStepForm

    def form_valid(self, form):
        user_data = self.request.session.get(f"{self.request.user.id}")
        user_data["address"] = form.cleaned_data["address"]
        user_data["city"] = form.cleaned_data["city"]
        user_data["delivery_type"] = form.cleaned_data["delivery_type"]
        self.request.session[f"{self.request.user.id}"] = user_data
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "не верный ввод полей")
        return super().form_invalid(form)


class ThirdOrderView(LoginRequiredMixin, FormView):
    template_name = "order/order_3.jinja2"
    form_class = ThirdStepForm
    success_url = reverse_lazy("url:step4")

    def form_valid(self, form):
        user_data = self.request.session.get(f"{self.request.user.id}")
        user_data["payment_type"] = form.cleaned_data["payment_type"]
        self.request.session[f"{self.request.user.id}"] = user_data

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "не верный ввод полей")
        return super().form_invalid(form)


class FourStepView(LoginRequiredMixin, ListView):
    template_name = "order/order_4.jinja2"
    model = ProductInCart

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=self.request.user.id)
        user = User.objects.get(pk=request.user.id)
        total_price = ProductInCart.objects.filter(cart=cart)[:3]
        db_price = 0
        for price in total_price:
            db_price += price.offer.price * price.quantity
        Order.objects.update_or_create(
            cart=cart,
            user=user,
            defaults={
                "phone": request.session[f"{self.request.user.id}"]["phone"],
                "name": request.session[f"{self.request.user.id}"]["name"],
                "delivery_type": request.session[f"{self.request.user.id}"]["delivery_type"],
                "city": request.session[f"{self.request.user.id}"]["city"],
                "address": request.session[f"{self.request.user.id}"]["address"],
                "payment_type": request.session[f"{self.request.user.id}"]["payment_type"],
                "total_price": db_price,
            },
        )
        return HttpResponseRedirect(reverse("user:profile"))

    def get_context_data(self, *, object_list=None, **kwargs):
        from .service import translate

        context = super().get_context_data(**kwargs)
        cart = Cart.objects.get(user=self.request.user.id)
        delivery_type, pay_type = translate(self.request.session[f"{self.request.user.id}"]["delivery_type"])
        comparison_list = get_comparison_list(self.request.user.id)
        comparison_count = len(comparison_list)

        context["delivery_type"] = delivery_type
        context["name"] = self.request.session[f"{self.request.user.id}"]["name"]
        context["phone"] = self.request.session[f"{self.request.user.id}"]["phone"]
        context["city"] = self.request.session[f"{self.request.user.id}"]["city"]
        context["address"] = self.request.session[f"{self.request.user.id}"]["address"]
        context["payment"] = pay_type
        context["product"] = ProductInCart.objects.filter(cart=cart)[:3]
        context["comparison_count"] = comparison_count
        return context
