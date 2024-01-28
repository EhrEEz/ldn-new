from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from .api import router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("v/", include(router.urls)),
    path("api/", include("apps.authentication.urls", namespace="authentication")),
    path("vehicles/", include("apps.vehicles.urls"), name="vehicles_urls"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
