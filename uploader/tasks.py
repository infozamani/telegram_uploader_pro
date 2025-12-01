# uploader/tasks.py — این فایل رو کامل بساز (اگر نیست)
import time
import threading
from django.utils import timezone
from .models import Post, Product
from .utils import send_to_telegram_post, send_to_telegram_product

def check_scheduled_items():
    """هر ۳۰ ثانیه چک می‌کنه پست و محصول زمان‌بندی شده بفرسته"""
    while True:
        now = timezone.localtime()
        
        # چک کردن پست‌های معمولی
        posts = Post.objects.filter(status='scheduled', scheduled_time__lte=now)
        for post in posts:
            if send_to_telegram_post(post):
                post.status = 'sent'
                post.sent_at = now
            else:
                post.status = 'failed'
            post.save()

        # چک کردن محصولات
        products = Product.objects.filter(status='scheduled', scheduled_time__lte=now)
        for product in products:
            if send_to_telegram_product(product):
                product.status = 'sent'
                product.sent_at = now
            else:
                product.status = 'failed'
            product.save()

        time.sleep(30)  # هر ۳۰ ثانیه چک کن

# این خط رو حتماً بذار تا وقتی سرور بالا میاد، تسک شروع بشه
threading.Thread(target=check_scheduled_items, daemon=True).start()