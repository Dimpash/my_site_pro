# my_site_pro/urls.py
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from cv.sitemaps import PublicSitemap
from cv.views import robots_txt


urlpatterns = [
    path('admin/', admin.site.urls),
    path("medical-bayes/", include("apps.medical_bayes.urls")),

    # robots.txt
    path("robots.txt", robots_txt, name="robots-txt"),

    # sitemap
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {"public": PublicSitemap}},
        name="django.contrib.sitemaps.views.sitemap",
    ),

    path('', include('cv.urls')),
    # path('', include(('genealogy.urls', 'genealogy'), namespace='genealogy')),
    path('genealogy/', include('genealogy.urls')),
    path('demo/', include('mail_detector.urls')),
    path('sandbox/', include('sandbox.urls')),


]
