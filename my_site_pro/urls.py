# my_site_pro/urls.py
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from cv.sitemaps import PublicSitemap

urlpatterns = [
    path('admin/', admin.site.urls),
    path("medical-bayes/", include("apps.medical_bayes.urls")),
    path('', include('cv.urls')),
    # path('', include(('genealogy.urls', 'genealogy'), namespace='genealogy')),
    path('genealogy/', include('genealogy.urls')),
    path('demo/', include('mail_detector.urls')),
    path('sandbox/', include('sandbox.urls')),

    # sitemap
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {"public": PublicSitemap}},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
