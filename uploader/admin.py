# uploader/admin.py — نسخه نهایی بدون هیچ خطایی
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Post, Product

# ———————————————— ادمین پست معمولی ————————————————
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'use_ai_caption', 'status_colored', 'send_now_button']
    list_filter = ['use_ai_caption', 'status']
    search_fields = ['title']

    def status_colored(self, obj):
        color = {'sent':'green', 'failed':'red', 'scheduled':'orange', 'draft':'gray'}.get(obj.status, 'black')
        return format_html('<b style="color:{}">● {}</b>', color, obj.get_status_display())
    status_colored.short_description = "وضعیت"

    def send_now_button(self, obj):
        if obj.status != 'sent':
            return format_html(
                '<a href="/send-post/{}/" style="background:#ff6b6b;color:white;padding:8px 16px;border-radius:8px;text-decoration:none;">ارسال پست</a>',
                obj.id
            )
        return format_html('<span style="color:green">ارسال شده</span>')
    send_now_button.short_description = "ارسال"


# ———————————————— ادمین محصول فروشگاه ————————————————
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_code', 'name', 'brand', 'final_price_display', 'use_ai_caption', 'status_colored', 'send_now_button']
    list_filter = ['use_ai_caption', 'in_stock', 'status']
    search_fields = ['product_code', 'name', 'brand']

    def final_price_display(self, obj):
        return f"{obj.final_price():,} تومان".replace(',', '٬')
    final_price_display.short_description = "قیمت نهایی"

    def status_colored(self, obj):
        color = {'sent':'green', 'failed':'red', 'scheduled':'orange', 'draft':'gray'}.get(obj.status, 'black')
        return format_html('<b style="color:{}">● {}</b>', color, obj.get_status_display())
    status_colored.short_description = "وضعیت"

    def send_now_button(self, obj):
        if obj.status != 'sent':
            return format_html(
                '<a href="/send-product/{}/" style="background:#00d4aa;color:white;padding:8px 16px;border-radius:8px;text-decoration:none;">ارسال محصول</a>',
                obj.id
            )
        return format_html('<span style="color:green">ارسال شده</span>')
    send_now_button.short_description = "ارسال"