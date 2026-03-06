from django.urls import path
from roamify import views
app_name = 'roamify'
urlpatterns = [
    path('', views.index, name='index'),
]
