from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_new_short_url, name='create_new_short_url'),
    path('ref/<unique_identifier_to_url>/',views.redirect_user, name='redirect_user')
]