"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django import views
from django.contrib import admin
from django.urls import path,include
from django.urls import path
from tickets.views import mixins_pk,rest_model_id,no_rest_no_model,no_rest_from_model,FBV_List,FBV_pk,CBV_List,CBV_pk,mixins_list

from tickets import views

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('guests', views.viewsets_guest)
router.register('movies', views.viewsets_movie)
router.register('reservations', views.viewsets_reservation)

urlpatterns = [
    path('admin/', admin.site.urls),

    #1
    path('jsonresponsenomodel',no_rest_no_model),
    #2
    path('jsonresponsefrommodel',no_rest_from_model),
    #3.1 GET POST from rest framework function based view @api_view
    path('rest/fbv/', FBV_List),
     #3.2 GET PUT DELETE from rest framework function based view @api_view
    path('rest/fbv/<int:pk>', FBV_pk),
    #4.1 
    path('rest/cbv/', CBV_List.as_view()),
    #4.2
    path('rest/cbv/<int:pk>', CBV_pk.as_view()),

    path('restmodelid',rest_model_id),

    #5.1
    path('rest/mixins',mixins_list.as_view()),
    #5.2
    path('rest/mixins/<int:pk>',mixins_pk.as_view()),
    #7
    path('rest/viewsets/', include(router.urls)),
    

    #6.1 GET POST from rest framework class based view generics
    path('rest/generics/', views.generics_list.as_view()),

    #6.2 GET PUT DELETE from rest framework class based view generics
    path('rest/generics/<int:pk>', views.generics_pk.as_view()),
    #8 find movie 
    path('fbv/findmovie', views.find_movie),
    #8.2
    path('fbv/newreservation',views.new_reservation),
    

]
