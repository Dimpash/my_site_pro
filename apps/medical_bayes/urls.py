from django.urls import path
from django.views.static import serve

from .views import medical_bayes
from django.conf import settings


urlpatterns = [
    path("", medical_bayes, name="medical_bayes"),

    path(
        "<path:path>",
        serve,
        {
            "document_root": settings.BASE_DIR / "apps" / "medical_bayes" / "static" / "medical_bayes",
        },
    ),
]