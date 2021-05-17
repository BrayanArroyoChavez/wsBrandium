from django.contrib import admin
from django.urls import path
from wsBrandiumDJ.views import inicio, busqueda, carga
from wsBrandiumDJ.static.scraping.main import scraping
from wsBrandiumDJ.static.scraping.detail import detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio),
    path('inicio/', inicio),
    path('carga/', carga),
    path('busqueda/', busqueda),
    path('scraping', scraping),
    path('scraping/detail', detail),
]
