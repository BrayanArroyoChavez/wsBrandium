from django.contrib import admin
from django.urls import path
from wsBrandiumDJ.views import inicio, busqueda, carga_detalle, carga_main
from wsBrandiumDJ.static.scraping.main import scraping
from wsBrandiumDJ.static.scraping.detail import detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio),
    path('inicio/', inicio),
    path('busqueda/', busqueda),
    path('busqueda/carga', carga_detalle),
    path('scraping', scraping),
    path('scraping/carga', carga_main),
    path('scraping/detail', detail),
]
