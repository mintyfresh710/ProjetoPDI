from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("app_pdi/", include("app_pdi.urls")),
    path("pdi_form/", include("pdi_form.urls")),
    path("", include("app_pdi.urls")),
]