from django.contrib import admin
from django.urls import path
from wsBrandiumDJ.views import inicio, busqueda
from wsBrandiumDJ.static.scraping.main import scraping
from wsBrandiumDJ.static.scraping.detail import detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inicio/', inicio),
    path('busqueda/', busqueda),
    path('scraping', scraping),
    path('scraping/detail', detail),
]
