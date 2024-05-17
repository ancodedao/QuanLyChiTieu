from django.urls import path
from app.views import login_view, register_view,home_view,nguoidung_view,lich_chi_tieu_view,delete_lich_chi_tieu,noidunglich_view,delete_noidunglich,thunhap_view,delete_thunhap,thongtin_chitieu,delete_thongtin_chitieu

urlpatterns = [
    path('', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('home/', home_view, name='home'),
    path('nguoidung/', nguoidung_view, name='nguoidung'),
    path('lichchitieu/', lich_chi_tieu_view, name='lich_chi_tieu'),
    path('lichchitieu/delete/<int:id>/', delete_lich_chi_tieu, name='delete_lich_chi_tieu'),
    path('noidunglich/<int:lich_id>/', noidunglich_view, name='noidunglich'),
    path('noidunglich/delete/<int:id>/', delete_noidunglich, name='delete_noidunglich'),
    path('thunhap/', thunhap_view, name='thunhap'),
    path('thunhap/delete/<int:id>/', delete_thunhap, name='delete_thunhap'),
    path('thongtinchiteu', thongtin_chitieu, name='thongtin_chitieu'),
    path('delete/<int:id>/', delete_thongtin_chitieu, name='delete_thongtin_chitieu'),
]
