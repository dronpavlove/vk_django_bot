from django.contrib import admin
from django.urls import path, include
from products.views import ProductDetailView, BaseProductListView

urlpatterns = [
    path('list/', BaseProductListView.as_view()),
    path('<int:pk>/', ProductDetailView.as_view()),
]