from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("medical-bayes/", include("apps.medical_bayes.urls")),
    path('', include('cv.urls')),
    # path('', include(('genealogy.urls', 'genealogy'), namespace='genealogy')),
    path('genealogy/', include('genealogy.urls')),
    path('demo/', include('mail_detector.urls')),
    path('sandbox/', include('sandbox.urls')),
]
