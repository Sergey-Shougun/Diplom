from django.urls import path
from . import views

urlpatterns = [
    path('submitData', views.submit_data, name='submit_data'),
    path('submitData/<int:pk>/', views.pereval_detail, name='pereval_detail'),
    path('submitData/', views.get_user_perevals, name='get_user_perevals'),
]