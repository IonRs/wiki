from django.urls import path

from . import views
app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("random/<str:TITLE>", views.random, name="random"),
    path("edit/<str:TITLE>", views.edit, name="edit"),
    path("<str:TITLE>", views.entry, name="entry")
]