from django .urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/', views.userhome, name='userhome'),
    path('register/', views.register, name = 'register'),
    path('', views.login_view, name='login'),
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
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)