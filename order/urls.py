from django.urls import path

from . import views

urlpatterns = [
    # ex: /home/
    path('', views.index, name='index'),
    path('addtocart/<int:id>',views.addtocart, name='addtocart'),
    path('deletefromcart/<int:id>',views.deletefromcart, name='deletefromcart'),


]
