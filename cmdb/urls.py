from . import views
from django.urls import path
from django.conf.urls import url,include

app_name = 'cmdb'

urlpatterns = [
    path('', views.table, name='table-url'),
    path('table/change/', views.change_table, name='change-table-url'),
    path('table/delete/', views.delete_table, name='delete-table-url'),
    path('table/detail/', views.detail_table, name='detail-url'),
    url(r'login/',views.acc_login ,name='login'),
    url(r'logout/',views.acc_logout,name="logout" ),
    url(r'register/',views.register,name="register" ),

]