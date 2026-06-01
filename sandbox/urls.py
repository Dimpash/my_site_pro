from django.urls import path 
from .views import fb_privacy, fb_terms, fb_data_deletion 


urlpatterns = [ 
    path("my-fb-privacy/", fb_privacy, name="fb_privacy"), 
    path("my-fb-terms/", fb_terms, name="fb_terms"), 
    path("my-fb-data-deletion/", fb_data_deletion, name="fb_data_deletion"), 
]