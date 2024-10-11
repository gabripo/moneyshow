from django.urls import path
from . import views

urlpatterns = [
    path(route="", view=views.home, name="home"),
    path("get_stock_data/", view=views.get_stock_data),
    path("clear_stock_data/", view=views.clear_stock_data),
]
