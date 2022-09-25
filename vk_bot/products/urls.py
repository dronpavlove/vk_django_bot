from django.contrib import admin
from django.urls import path, include
from products.views import ProductDetailView, BaseProductListView
from bot_logic.vk_bot_logic import update_data

urlpatterns = [
    path('list/', BaseProductListView.as_view()),
    path('<int:pk>/', ProductDetailView.as_view()),
    path('update_cache', update_data)
]