from django.urls import path

from catalog import views

app_name = "catalog"

urlpatterns = [
    path("categories/", views.category_list, name="category_list"),
]
