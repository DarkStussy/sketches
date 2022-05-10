from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('order/<int:serv_id>/', views.order, name='order_by_id'),
    path('order/', views.order, name='order'),
    path('favorite_add/<int:img_id>/', views.favorite_add, name='favorite_add'),
    path('favorite_delete/<int:fv_id>/<int:photo_id>/', views.favorite_delete, name='favorite_delete'),
    path('add_example_image/', views.add_example_image, name='add_example_image'),
]
