from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='index'),
    path('category/<slug:slug>/', views.ProductsByCategoryView.as_view(), name='category'),
    path('detail/<slug:slug>/', views.ProductDetailView.as_view(), name='detail'),
]
