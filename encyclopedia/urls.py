from django.urls import path

from . import views
app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("edit", views.edit, name="edit"),
    path("<str:TITLE>", views.entry, name="entry")
]