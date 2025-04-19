from django .urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/', views.userhome, name='userhome'),
    path('register/', views.register, name = 'register'),
    path('doctor-register/', views.doctor_registration, name = 'doctor_register'),
    path('login', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('kyk/', views.kyk, name='kyk'),
    path('adminbase/', views.adminbase, name='adminbase'),
    path('features/', views.feature_list, name='feature_list'),
    path('add-feature/', views.add_feature, name='add_feature'),
    path('edit-feature/<int:id>/', views.edit_feature, name='edit_feature'),
    path('delete-feature/<int:id>/', views.delete_feature, name='delete_feature'),
    path('faq/', views.faq, name='faq'),
    path('admin-faq/', views.admin_faq, name='admin_faq'),
    path('admin-faqs/delete/<int:id>/', views.delete_faq, name='delete_faq'),
    path('admin-dialysis-centers/', views.add_dcenter, name='add_dcenter'),
    path('admin-dialysis-centers/edit/<int:center_id>/', views.edit_dcenter, name='edit_dcenter'),
    path('admin-dialysis-centers/delete/<int:center_id>/', views.delete_dcenter, name='delete_dcenter'),
    path('dialysis-centers/', views.dialysis_center, name='dialysis_center'),
    path('gfr/', views.gfr, name='gfr'),
    path('diet/', views.diet, name='diet'),
    path('admin-add-hospitals/edit/<int:hosp_id>/', views.edit_hosp, name = 'edit_hospitals'),
    path('admin-add-hospitals/delete/<int:hosp_id>/', views.delete_hosp, name = 'dlt_hospitals'),
    path('admin-add-hospitals/', views.add_hospital, name = 'add_hospitals'),
    path('hospitals/', views.hospital_list, name='hospital_list'),
    path('doctor-dashboard/', views.doctor_dashboard, name = 'doctor_dashboard'),
    path('doctors/<int:hosp_id>/', views.doctor_list, name = 'doctors_list'),
    path('toggle-status/', views.toggle_doctor_status, name='toggle_doctor_status'),
    path('booking/<int:doctor_id>/',views.book, name='book'),
    path('profile/', views.profile_view, name='profile'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)