
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from new_app import views

urlpatterns = [
    path('', views.index, name="index"),
    path('dashbord/', views.dashbord, name="dashbord"),
    path('register/', views.register_request, name="register"),
    path('view_members/', views.view_members, name="view_members"),
    path('login/', views.login_request, name="login"),
    path('logout/', views.logout_request, name="logout"),
    path('view_card/<int:id>/', views.view_card, name="print"),
    path('delete_user/<int:id>/', views.delete_user, name="delete_user"),
    path('update_user/<int:id>/', views.update_user_admin, name="update_user"),
    path('ajax/', views.ajax_fun, name="ajax"),
    path('profile/<int:id>/', views.profile, name="profile"),
    path('add_blood_donate/', views.add_blood_donate, name="add_blood_donate"),
    path('view_blood_donate/', views.view_blood_donate, name="view_blood_donate"),
    path('verify_blood_donator/<int:id>/', views.verify_blood_donator, name="verify_blood_donator"),
    path('view_contacts/', views.view_contacts, name="view_contacts"),
    path('add_activity/', views.add_activity, name="add_activity"),
    path('view_activities/', views.view_activity, name="view_activities"),
    path('add_district/', views.add_district, name="add_district"),
    path('view_district/', views.view_district, name="view_district"),
    path('add-ac-setting/', views.add_ac_setting, name="add-ac-setting"),
    path('view-ac-setting/', views.view_ac_setting, name="view-ac-setting"),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
