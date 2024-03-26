"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from market.config import settings

urlpatterns = [
    path("admin/settings_app/", include("settings_app.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls", namespace="user")),
    path("cart/", include("cart.urls", namespace="cart")),
    path("discounts/", include("discounts.urls", namespace="discount")),
    path("", include(("products.urls", "products"), namespace="product")),
    path("pay/", include("order.urls", namespace="url")),
    path("", include(("imports.urls", "imports"), namespace="imports")),
    path("comparison/", include(("comparison.urls", "comparison"), namespace="comparison")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
