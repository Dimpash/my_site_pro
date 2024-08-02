from django.urls import path
from .views import *

urlpatterns = [
    path('cv_index/<lang>', cv_index, name="cv-index"),
    path('', cv_index, name="cv-start-0"),
    path('<lang>', cv_start, name="cv-start"),
    path('portfolio_details/<lang>/<portfolio_name>', portfolio_details, name="portfolio-details"),
]