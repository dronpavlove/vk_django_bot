from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import bot_logic.views as bot

urlpatterns = [
    path('', bot.index),
    # path('products/', include('products.urls')),
]