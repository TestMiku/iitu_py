from django.urls import path
from .views import add_data, success, show_data, edit_data, delete_data


urlpatterns = [
    path('add/', add_data, name='add_data'),
    path('success/', success, name='success'),
    path('show/', show_data, name='show_data'),
    path('edit/<int:pk>/', edit_data, name='edit_data'),
    path('delete/<int:pk>/', delete_data, name='delete_data'),
]