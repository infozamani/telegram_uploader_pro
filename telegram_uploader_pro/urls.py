# telegram_uploader_pro/urls.py
from django.contrib import admin
from django.urls import path, include  # <-- include را اضافه کنید
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect  # <-- برای ریدایرکت
from uploader import views as uploader_views

urlpatterns = [
    # مسیر ریشه - مستقیماً به لاگین می‌رود
    path("", lambda request: redirect("login"), name="root"),
    
    path("admin/", admin.site.urls),
    path(
        "login/", 
        auth_views.LoginView.as_view(template_name="login.html"), 
        name="login"
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", uploader_views.dashboard, name="dashboard"),
    
    # فرم‌ها
    path("upload-post/", uploader_views.upload_post, name="upload_post"),
    path("upload-product/", uploader_views.upload_product, name="upload_product"),
    
    # پیش‌نمایش و تأیید محصول
    path("preview-product/", uploader_views.preview_product, name="preview_product"),
    path("confirm-product/", uploader_views.confirm_product, name="confirm_product"),
]

# برای نمایش عکس‌های موقت (temp)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)