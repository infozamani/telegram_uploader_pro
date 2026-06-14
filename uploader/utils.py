import html
import asyncio
from telegram import Bot
from django.conf import settings
import google as genai

 
# تنظیم Gemini یک بار
try:
    genai.configure(api_key=settings.GEMINI_API_KEY)
except:
    pass


# ——————————————————————————————
# تابع ۱: ارسال پست معمولی (عکس/ویدیو/فایل + کپشن هوش مصنوعی یا دستی)
# ——————————————————————————————
async def generate_simple_caption(image_path):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        img = genai.upload_file(image_path)
        response = model.generate_content(
            [
                img,
                "یه کپشن جذاب، فارسی، پر از ایموجی و احساسی برای این عکس/ویدیو بنویس. حداکثر ۴ خط. فقط متن کپشن رو بده.",
            ]
        )
        return response.text.strip()
    except Exception as e:
        print("خطا در تولید کپشن:", e)
        return "عکس فوق‌العاده زیبا"


def send_to_telegram_post(post):
    bot = Bot(token=settings.BOT_TOKEN)

    # ساخت کپشن
    caption = post.caption.strip() if post.caption.strip() else ""
    if post.use_ai_caption and not caption and post.media_file:
        caption = asyncio.run(generate_simple_caption(post.media_file.path))

    if post.hashtags:
        caption += "\n\n" + post.hashtags

    try:
        with open(post.media_file.path, "rb") as f:
            file_path = post.media_file.path
            ext = file_path.lower().split(".")[-1]

            if ext in ["jpg", "jpeg", "png", "gif", "webp"]:
                asyncio.run(
                    bot.send_photo(
                        chat_id=settings.CHANNEL_ID,
                        photo=f,
                        caption=caption or "عکس زیبا",
                    )
                )
            elif ext in ["mp4", "mov", "avi", "mkv"]:
                asyncio.run(
                    bot.send_video(
                        chat_id=settings.CHANNEL_ID,
                        video=f,
                        caption=caption or "ویدیوی جذاب",
                    )
                )
            else:
                asyncio.run(
                    bot.send_document(
                        chat_id=settings.CHANNEL_ID,
                        document=f,
                        caption=caption or "فایل",
                    )
                )
        return True
    except Exception as e:
        print("خطا در ارسال پست معمولی:", e)
        return False


async def generate_product_ai_caption(image_path):
    """تولید کپشن حرفه‌ای با Gemini — نسخه ۱۰۰٪ کارکردنی"""
    try:
        # درست‌ترین روش برای ارسال عکس لوکال به Gemini
        from pathlib import Path

        sample_file = genai.upload_file(path=image_path, display_name="product_image")

        # صبر می‌کنیم تا آپلود کامل بشه (مهم!)
        while sample_file.state.name == "PROCESSING":
            print("در حال پردازش عکس توسط Gemini...")
            await asyncio.sleep(2)
            sample_file = genai.get_file(sample_file.name)

        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = """
        تو یک ادمین حرفه‌ای کانال فروشگاهی لوکس هستی.
        یک کپشن تبلیغاتی کوتاه (حداکثر ۳ خط)، احساسی، جذاب و پر از ایموجی برای این محصول بنویس.
        فقط متن کپشن رو بده، بدون هیچ توضیح اضافه.
        """

        response = model.generate_content([sample_file, prompt])
        return response.text.strip()

    except Exception as e:
        print(f"خطا در Gemini: {e}")
        return "محصول لوکس و بی‌نظیر"


def send_to_telegram_product(product):
    if product.status == "sent":
        return True  # دیگه کاری نکن
    bot = Bot(token=settings.BOT_TOKEN)

    # تولید کپشن هوش مصنوعی (فقط اگر تیک زده باشه و هنوز نداشته باشه)
    if product.use_ai_caption and not product.ai_caption and product.media_file:
        try:
            print("در حال تولید کپشن با هوش مصنوعی...")
            product.ai_caption = asyncio.run(
                generate_product_ai_caption(product.media_file.path)
            )
            product.save(update_fields=["ai_caption"])
            print("کپشن هوش مصنوعی با موفقیت تولید شد!")
        except Exception as e:
            print(f"خطا در تولید کپشن: {e}")
            product.ai_caption = "محصول باکیفیت و خاص"

    # کپشن نهایی
    caption_text = product.ai_caption or "محصول جدید و جذاب"

    # ساخت پیام حرفه‌ای
    specs = ""
    if product.brand:
        specs += f"\n🏷 برند: {product.brand}"
    specs += f"\nموجودی: {'دارد' if product.in_stock else 'ناموجود'}"

    if product.discount_percent > 0:
        specs += (
            f"\n❌ قیمت اصلی: <s>{int(product.original_price):,}</s> تومان".replace(
                ",", "٬"
            )
        )
        specs += f"\n🔥  تخفیف: {product.discount_percent}٪"
        specs += (
            f"\n✅  <b>قیمت نهایی: {int(product.final_price()):,} تومان</b>".replace(
                ",", "٬"
            )
        )
    else:
        specs += f"\n💰 قیمت: {int(product.original_price):,} تومان".replace(",", "٬")

    if product.delivery_days:
        specs += f"\n🚚  ارسال: {product.delivery_days}"

    full_caption = f"""<b>{html.escape(product.name)}</b>

{html.escape(caption_text)}

━━━━━━━━━━━━{specs}

🆔 @aitelgram499"""

    try:
        with open(product.media_file.path, "rb") as f:
            asyncio.run(
                bot.send_photo(
                    chat_id=settings.CHANNEL_ID,
                    photo=f,
                    caption=full_caption,
                    parse_mode="HTML",
                )
            )
        return True
    except Exception as e:
        print(f"خطا در ارسال به تلگرام: {e}")
        return False
