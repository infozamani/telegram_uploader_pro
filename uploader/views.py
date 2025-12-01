# uploader/views.py — نسخه نهایی، تمیز، کامل و ۱۰۰٪ کارکردنی
import os
import uuid
import html
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone

# مدل‌ها
from .models import Post, Product

# توابع ارسال
from .utils import send_to_telegram_post, send_to_telegram_product


# ——————————————————————
# داشبورد اصلی
# ——————————————————————
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


# ——————————————————————
# آپلود پست معمولی (بدون پیش‌نمایش — مستقیم ارسال)
# ——————————————————————
@login_required
def upload_post(request):
    if request.method == 'POST':
        try:
            post = Post.objects.create(
                media_file=request.FILES['media_file'],
                caption=request.POST.get('caption', '').strip(),
                use_ai_caption='use_ai_caption' in request.POST,
                hashtags=request.POST.get('hashtags', '').strip()
            )

            if send_to_telegram_post(post):
                post.status = 'sent'
                post.sent_at = timezone.now()
                post.save()
                messages.success(request, "پست با موفقیت به کانال ارسال شد!")
            else:
                post.status = 'failed'
                post.save()
                messages.error(request, "خطا در ارسال پست به تلگرام!")

        except Exception as e:
            messages.error(request, f"خطا در ارسال پست: {e}")

        return redirect('dashboard')

    return render(request, 'upload_post.html')


# ——————————————————————
# آپلود محصول (با پیش‌نمایش حرفه‌ای — کاملاً تست شده!)
# ——————————————————————
@login_required
def upload_product(request):
    # فقط نمایش فرم
    return render(request, 'upload_product.html')


@login_required
def preview_product(request):
    if request.method != 'POST':
        return redirect('upload_product')

    try:
        # دریافت اطلاعات فرم
        data = {
            'product_code': request.POST['product_code'].strip(),
            'name': request.POST['name'].strip(),
            'brand': request.POST.get('brand', '').strip(),
            'original_price': int(request.POST['original_price']),
            'discount_percent': int(request.POST.get('discount_percent', 0)),
            'in_stock': request.POST.get('in_stock', '1') == '1',
            'delivery_days': request.POST.get('delivery_days', '۳ تا ۵ روز کاری').strip(),
            'use_ai_caption': 'use_ai_caption' in request.POST,
        }

        # ذخیره موقت عکس
        file = request.FILES['media_file']
        os.makedirs('media/temp', exist_ok=True)
        temp_filename = f"prod_{uuid.uuid4().hex}_{file.name}"
        temp_path = f"media/temp/{temp_filename}"
        with open(temp_path, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)

        # ذخیره در سشن
        request.session['temp_product_data'] = data
        request.session['temp_product_image'] = temp_filename

        # ساخت کپشن پیش‌نمایش
        caption = f"<b>{html.escape(data['name'])}</b>\n\n"
        caption += "در حال تولید کپشن لوکس توسط هوش مصنوعی...\n\n" if data['use_ai_caption'] else "محصول باکیفیت و خاص\n\n"
        caption += "━━━━━━━━━━━━\n"
        caption += f"برند: {data['brand'] or '—'}\n"
        caption += f"موجودی: {'دارد' if data['in_stock'] else 'ناموجود'}\n"

        if data['discount_percent'] > 0:
            old = f"{data['original_price']:,}".replace(',', '٬')
            final = int(data['original_price'] * (100 - data['discount_percent']) / 100)
            final_str = f"{final:,}".replace(',', '٬')
            caption += f"قیمت اصلی: <s>{old}</s> تومان\n"
            caption += f"تخفیف: {data['discount_percent']}٪\n"
            caption += f"<b>قیمت نهایی: {final_str} تومان</b>\n"
        else:
            price = f"{data['original_price']:,}".replace(',', '٬')
            caption += f"قیمت: {price} تومان\n"

        caption += f"ارسال: {data['delivery_days']}\n\n@aitelgram499"

        return render(request, 'preview_product.html', {
            'media_url': f'/media/temp/{temp_filename}',
            'caption': caption,
        })

    except Exception as e:
        messages.error(request, f"خطا در پیش‌نمایش: {e}")
        return redirect('upload_product')


@login_required
def confirm_product(request):
    if request.method != 'POST':
        return redirect('dashboard')

    data = request.session.get('temp_product_data')
    image_filename = request.session.get('temp_product_image')

    if not data or not image_filename:
        messages.error(request, "جلسه منقضی شده! دوباره امتحان کن.")
        return redirect('upload_product')

    try:
        # چک تکراری بودن شماره محصول
        if Product.objects.filter(product_code=data['product_code']).exists():
            messages.error(request, f"شماره محصول «{data['product_code']}» قبلاً استفاده شده!")
            return redirect('upload_product')

        # ایجاد محصول واقعی
        product = Product.objects.create(
            product_code=data['product_code'],
            name=data['name'],
            brand=data['brand'],
            original_price=data['original_price'],
            discount_percent=data['discount_percent'],
            in_stock=data['in_stock'],
            delivery_days=data['delivery_days'],
            media_file=f"temp/{image_filename}",
            use_ai_caption=data['use_ai_caption']
        )

        # ارسال به کانال
        if send_to_telegram_product(product):
            product.status = 'sent'
            product.sent_at = timezone.now()
            product.save()
            messages.success(request, f"محصول «{product.name}» با موفقیت ارسال شد!")
        else:
            product.status = 'failed'
            product.save()
            messages.error(request, "خطا در ارسال به تلگرام!")

        # پاکسازی
        try:
            os.remove(f"media/temp/{image_filename}")
        except:
            pass

        # پاک کردن سشن
        request.session.pop('temp_product_data', None)
        request.session.pop('temp_product_image', None)

    except Exception as e:
        messages.error(request, f"خطای ذخیره: {e}")

    return redirect('dashboard')


# ——————————————————————
# ویوهای ادمین (ارسال دستی از پنل)
# ——————————————————————
@staff_member_required
def send_post_now(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.status != 'sent':
        if send_to_telegram_post(post):
            post.status = 'sent'
            post.sent_at = timezone.now()
            post.save()
            messages.success(request, "پست ارسال شد!")
    return redirect('admin:uploader_post_changelist')


@staff_member_required
def send_product_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.status != 'sent':
        if send_to_telegram_product(product):
            product.status = 'sent'
            product.sent_at = timezone.now()
            product.save()
            messages.success(request, "محصول ارسال شد!")
    return redirect('admin:uploader_product_changelist')