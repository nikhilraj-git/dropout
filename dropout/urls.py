from django.urls import path
from . import views
from django.urls import path
from .views import CustomLoginView, CustomLogoutView
from .views import upload_file

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('export-csv/', views.export_csv, name='export_csv'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
        path('upload/', upload_file, name='upload'),

]