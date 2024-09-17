from django.urls import path
from . import views

urlpatterns = [path(route="", view=views.stock_list, name="stock_list")]
