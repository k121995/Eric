from django.urls import path
from . import views	


app_name = 'testapp'  # here for namespacing of urls.

urlpatterns = [
    # path("", views.Home, name="home"),
    path('', views.login_request, name="login"),
    path('upload/csv/', views.upload_csv, name="upload_csv"),
]