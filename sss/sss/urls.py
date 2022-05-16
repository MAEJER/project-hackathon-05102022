
from django.contrib import admin
from django.urls import path, include
from app import views

urlpatterns = [
    # Path to access the admin page
    path('admin/', admin.site.urls),
    # Path to access the home page
    path('', views.frontend, name="frontend"),
    # Path Login/Logout
    path('login/', include('django.contrib.auth.urls')),

    # ===============
    # BACKEND SECTION
    # ===============
    path('backend/', views.backend, name="backend"),

    # ===============
    # BACKEND SECTION
    # ===============
    path('home/', views.home, name="home"),

]
