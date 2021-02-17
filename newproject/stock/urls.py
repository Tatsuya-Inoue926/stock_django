from django.urls import path
from . import views

app_name = "stock"

urlpatterns = [
    path("", views.index, name="index"),
    path('result/', views.plt_svg, name='plot'),
    #path("candle/", views.mpf_svg, name="plot2"),
]