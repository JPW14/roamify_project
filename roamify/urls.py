from django.urls import path
from roamify import views
from django.contrib.auth import views as auth_views

app_name = 'roamify'

urlpatterns = [
    path('', views.index, name='index'),
    path('post/', views.post, name='post'),
    path('destination/<int:place_id>/', views.destination, name='destination'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='roamify/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
]