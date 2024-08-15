from django.urls import path
from .views import *

urlpatterns = [
    path('menu', genealogy_menu, name="menu"),
    path('accounts/login/', login_view, name="login"),
    path('auth', auth, name="auth"),
    path('logout', logout_user, name="logout"),
    path('genealogy_data_reload', genealogy_data_reload, name="genealogy-data-reload"),
    path('persons', PersonsListView.as_view(), name="persons"),
    path('personal_card/<int:pk>', PersonalCardDetailView.as_view(), name="personal-card"),
    path('descendants', descendants, name="descendants"),
    path('ancestors', ancestors, name="ancestors"),
]