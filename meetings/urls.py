from django.urls import path
from . import views


urlpatterns = [
    path('<int:id>', views.index, name="index"),
    path('<int:id>/edit', views.edit_object, name="edit"),
    path('<int:id>/delete', views.delete_object, name="delete"),
    path('new', views.new, name="new"),
    path('confirmation', views.confirm_delete, name="confirmation"),
    path('search', views.search_form, name="search")

]