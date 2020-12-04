from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
   	path("add/", views.add, name="add"),
   	path("apology/", views.apology, name="apology"),
   	path("ranarticle/", views.ranarticle, name="ranarticle"),
   	path("<str:name>", views.greet, name="greet"),
   	path("wiki/<str:name>", views.greet, name="greet"),
   	path("edit/", views.edit, name="edit"),
   	path("wiki/edit/", views.edit, name="edit")
  
]
 	