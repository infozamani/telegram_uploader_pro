# uploader/views.py — نسخه نهایی
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from .models import Post, Product
from .utils import send_to_telegram_post, send_to_telegram_product


@staff_member_required
def send_post_now(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.status == "sent":
        messages.info(request, "این پست قبلاً ارسال شده!")
    else:
        if send_to_telegram_post(post):
            post.status = "sent"
            post.sent_at = timezone.now()
            messages.success(
                request, f"پست «{post.title or post.id}» با موفقیت ارسال شد!"
            )
        else:
            post.status = "failed"
            messages.error(request, "خطا در ارسال پست!")
    post.save()
    return redirect("admin:uploader_post_changelist")


@staff_member_required
def send_product_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.status == "sent":
        messages.info(request, "این محصول قبلاً ارسال شده!")
    else:
        if send_to_telegram_product(product):
            product.status = "sent"
            product.sent_at = timezone.now()
            messages.success(
                request, f"محصول {product.product_code} - {product.name} ارسال شد!"
            )
        else:
            product.status = "failed"
            messages.error(request, "خطا در ارسال محصول!")
    product.save()
    return redirect("admin:uploader_product_changelist")


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages


@login_required
def dashboard(request):
    return render(request, "dashboard.html")


@login_required
def upload_post(request):
    messages.info(request, "فرم پست معمولی به زودی آماده میشه!")
    return render(request, "dashboard.html")


@login_required
def upload_product(request):
    messages.info(request, "فرم محصول فروشگاه به زودی آماده میشه!")
    return render(request, "dashboard.html")
