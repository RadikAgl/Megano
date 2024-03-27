from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from cart.models import Cart
from order.models import Order


User = get_user_model()


class OrderListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username="testuser", password="12345")
        test_user.save()
        number_of_orders = 5
        for order_id in range(number_of_orders):
            cart = Cart.objects.create(user=test_user)
            Order.objects.create(
                name=f"Test Order {order_id}",
                phone="1234567890",
                user=test_user,
                city="Test City",
                address="Test Address",
                total_price=100.00,
                cart_id=cart.id,
            )

    def setUp(self):
        self.client = Client()

    def test_order_list_view_for_logged_in_user(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("url:history_order"))
        self.assertEqual(response.status_code, 302)
        if response.context is not None:
            self.assertTrue("orders" in response.context)
            self.assertEqual(len(response.context["orders"]), 5)

    def test_order_list_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse("url:history_order"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))


class OrderDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username="testuser", password="12345")
        test_user.save()
        cart = Cart.objects.create(user=test_user)
        cls.test_order = Order.objects.create(
            name="Test Order",
            phone="1234567890",
            user=test_user,
            city="Test City",
            address="Test Address",
            total_price=100.00,
            cart_id=cart.id,
        )

    def setUp(self):
        self.client = Client()

    def test_order_detail_view_for_logged_in_user(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("url:detail_order", kwargs={"pk": self.test_order.pk}))
        self.assertEqual(response.status_code, 302)
