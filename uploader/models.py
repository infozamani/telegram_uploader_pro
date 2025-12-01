# uploader/models.py — هر دو مدل همزمان (Product + Post)
from django.db import models
from django.utils import timezone

# مدل پست معمولی (عکس، ویدیو، فایل)
class Post(models.Model):
    title = models.CharField(max_length=200, blank=True, verbose_name="عنوان (اختیاری)")
    media_file = models.FileField(upload_to='posts/', verbose_name="فایل (عکس/ویدیو/سند)")
    caption = models.TextField(blank=True, verbose_name="کپشن دستی")
    use_ai_caption = models.BooleanField(default=False, verbose_name="کپشن را هوش مصنوعی بنویسد؟")
    
    hashtags = models.CharField(max_length=500, blank=True, verbose_name="هشتگ‌ها")
    scheduled_time = models.DateTimeField(null=True, blank=True, verbose_name="زمان‌بندی")
    
    status = models.CharField(max_length=10, choices=[
        ('draft','پیش‌نویس'),('scheduled','زمان‌بندی'),('sent','ارسال شد'),('failed','ناموفق')
    ], default='draft')
    # فقط این دو خط رو تو هر دو مدل (Post و Product) داشته باش:
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="ساخته شده در")
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name="ارسال شده در")

    def __str__(self):
        return self.title or f"پست {self.id}"

    class Meta:
        verbose_name = "پست معمولی"
        verbose_name_plural = "پست‌های معمولی"


class Product(models.Model):
    product_code = models.CharField(max_length=30, unique=True, verbose_name="شماره محصول")
    name = models.CharField(max_length=200, verbose_name="نام محصول")
    brand = models.CharField(max_length=100, blank=True, verbose_name="برند")

    original_price = models.PositiveIntegerField(verbose_name="قیمت اصلی (تومان)")
    discount_percent = models.PositiveIntegerField(default=0, verbose_name="درصد تخفیف")
    
    in_stock = models.BooleanField(default=True, verbose_name="موجودی دارد؟")
    delivery_days = models.CharField(max_length=50, default="۳ تا ۵ روز کاری", verbose_name="زمان ارسال")

    media_file = models.FileField(upload_to='products/', verbose_name="عکس محصول")
    
    # ←←← این خط جدید رو اضافه کن
    ai_caption = models.TextField(blank=True, verbose_name="کپشن هوش مصنوعی (خودکار)")

    use_ai_caption = models.BooleanField(default=True, verbose_name="کپشن را هوش مصنوعی بنویسد؟")
    hashtags = models.CharField(max_length=500, blank=True, verbose_name="هشتگ‌ها")
    admin_id = models.CharField(max_length=50, default="@aitelgram499", verbose_name="آیدی ادمین")

    scheduled_time = models.DateTimeField(null=True, blank=True, verbose_name="زمان‌بندی")
    status = models.CharField(max_length=10, choices=[
        ('draft','پیش‌نویس'),('scheduled','زمان‌بندی'),('sent','ارسال شد'),('failed','ناموفق')
    ], default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    def final_price(self):
        if self.discount_percent > 0:
            return int(self.original_price * (100 - self.discount_percent) / 100)
        return self.original_price

    def __str__(self):
        return f"{self.product_code} - {self.name}"