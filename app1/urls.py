from django .urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # User urls
    path('register/', views.register, name = 'register'),
    path('login', views.login_view, name='login'),
    path('', views.userhome, name='userhome'),
    path('faq/', views.faq, name='faq'),
    path('kyk/', views.kyk, name='kyk'),
    path('diet/', views.diet, name='diet'),
    path('diet/<int:stage_id>/', views.stage_detail, name='stage_detail'),
    path('gfr/', views.gfr, name='gfr'),
    path('dialysis-centers/', views.dialysis_center, name='dialysis_center'),
    path('hospitals/', views.hospital_list, name='hospital_list'),
    path('doctors/<int:hosp_id>/', views.doctor_list, name = 'doctors_list'),
    path('booking/<int:doctor_id>/',views.book, name='book'),
    path('medicines/', views.medicine_store, name='medicine_store'),
    path('medicine/<int:id>/', views.medicine_detail, name='medicine_details'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart-item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('delete-cart-item/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('select-address/', views.select_address, name='select_address'),
    path('confirm-order/', views.confirm_order, name='confirm_order'),
    path('order-success/', views.order_success, name='order_success'),
    path('profile/', views.profile_view, name='profile'),

    # Doctor urls
    path('doctor-register/', views.doctor_registration, name = 'doctor_register'),
    path('doctor-dashboard/', views.doctor_dashboard, name = 'doctor_dashboard'),
    path('doctor/mark-completed/<int:appt_id>/', views.mark_completed, name='mark_completed'),
    path('toggle-status/', views.toggle_doctor_status, name='toggle_doctor_status'),

    # Admin urls
    path('adminhome/', views.admin_home, name='admin_home'),
    path('adminbase/', views.adminbase, name='adminbase'),
    path('admin-features/', views.feature_list, name='feature_list'),
    path('add-feature/', views.add_feature, name='add_feature'),
    path('edit-feature/<int:id>/', views.edit_feature, name='edit_feature'),
    path('delete-feature/<int:id>/', views.delete_feature, name='delete_feature'),
    path('admin-faq/', views.admin_faq, name='admin_faq'),
    path('admin-faqs/delete/<int:id>/', views.delete_faq, name='delete_faq'),
    path('admin-diet/add-stage/', views.add_stage, name='add_stage'),
    path('admin-diet/add-diet/', views.add_diet_plan, name='add_diet_plan'),
    path('admin-diet/add-workout/', views.add_workout_plan, name='add_workout_plan'),
    path('admin-dialysis-centers/', views.add_dcenter, name='add_dcenter'),
    path('admin-dialysis-centers/edit/<int:center_id>/', views.edit_dcenter, name='edit_dcenter'),
    path('admin-dialysis-centers/delete/<int:center_id>/', views.delete_dcenter, name='delete_dcenter'),
    path('admin-add-hospitals/', views.add_hospital, name = 'add_hospitals'),
    path('admin-add-hospitals/edit/<int:hosp_id>/', views.edit_hosp, name = 'edit_hospitals'),
    path('admin-add-hospitals/delete/<int:hosp_id>/', views.delete_hosp, name = 'dlt_hospitals'),
    path('admin-doctors/', views.admin_doctors, name='admin_doctors'),
    path('admin-doctors/view/<int:doctor_id>/', views.admin_doctor_view, name='admin_doctor_view'),
    path('admin-doctors/edit/<int:doctor_id>/', views.admin_doctor_edit, name='admin_doctor_edit'),
    path('admin-doctors/delete/<int:doctor_id>/', views.admin_doctor_delete, name='admin_doctor_delete'),
    path('admin-appointments/', views.admin_appointments, name='admin_appointments'),
    path('admin-medicine/', views.add_medicine, name='add_medicine'),
    path('admin-orders/', views.orders_view, name='orders'),

    path('logout/', views.logout_view, name='logout'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)