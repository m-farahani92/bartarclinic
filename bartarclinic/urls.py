"""
URL configuration for bartarclinic project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main_app.views import *
from django.conf import settings
from django.conf.urls.static import static
from main_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name=" "),
    path('therapy/', therapy),
    path('workshop/', workshop),
    path('categoryw/<adad>', categoryw),
    path('addcart/<adad>/', addcart),
    path('confirmPayment/',confirm_payment,name="confirmPayment"),
     path('admin/approve_reservation/<reservation_id>/', views.admin_approve_reservation, name='admin_approve_reservation'),
    path('reservation/', reservation,name="reservation"),
    path('addreservation/<adad>/', addreservation,name="addreservation"),
    path('deletecartR/<itmid>/', deletecartR,name="deletecartR"),
    path('deletecart/<itmid>/', deletecart,name="deletecart"),
    path('cart/', cart),
    path('checkoutR/', checkoutR),
    path('checkout/', checkout),
    path('team/', team),
    path('about/', about),
    path('contact/', contact),
    path('psychopathy/', psychopathy),
    path('test/', test),
    path('article/', article),
    path('gallery/', gallery),
    path('register/', register),
    path('login/', login ,name="login"),
    path('popup_login/', popup_login),
    path('logout/', logout ,name="logout"),
    path('dashboard/', dashboard ,name="dashboard"),
    path('panel/', panel ,name="panel"),
    path("get-schedule/", views.get_schedule_by_therapist, name="get_schedule"),
   
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
