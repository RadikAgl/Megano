# views.py
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View

from .forms import SiteSettingsForm
from .models import SiteSettings


@staff_member_required
def edit_settings(request):
    template_name = "settings_app/settings.html"
    site_settings = SiteSettings.objects.get_instance()

    if request.method == "POST":
        form = SiteSettingsForm(request.POST, instance=site_settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Settings updated successfully")
            return redirect(reverse_lazy("admin:settings_app"))

    else:
        form = SiteSettingsForm(instance=site_settings)

    context = {
        "form": form,
        "site_settings": site_settings,
        "app_label": "settings_app",
    }

    print(form.errors)
    print(context)
    return render(request, template_name, context)


@method_decorator(staff_member_required, name="dispatch")
class ResetCacheView(View):
    template_name = "settings_app/reset_cache.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        cache.clear()
        messages.success(request, "All cache is cleared")
        # Redirect to the main admin page
        return redirect(reverse("admin:index"))
