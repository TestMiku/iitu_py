from django.urls import path, include

urlpatterns = [
    path('nomenclature/', include('nomenclature.urls')),
]
