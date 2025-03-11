from django .urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/', views.userhome, name='userhome'),
    path('kyk/', views.kyk, name='kyk'),
    path('', views.adminbase, name='adminbase'),
    path('features/', views.feature_list, name='feature_list'),
    path('add-feature/', views.add_feature, name='add_feature'),
    path('edit-feature/<int:id>/', views.edit_feature, name='edit_feature'),
    path('delete-feature/<int:id>/', views.delete_feature, name='delete_feature'),
    path('faq/', views.faq, name='faq'),
    path('admin-faq/', views.admin_faq, name='admin_faq'),
    path('admin-faqs/delete/<int:id>/', views.delete_faq, name='delete_faq'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)