## 🇮🇷 <span id="fa">نسخه فارسی</span>

### 📌 معرفی پروژه

**Telegram Uploader Pro** یک اپلیکیشن تحت وب مبتنی بر **Django** است که به شما امکان می‌دهد:

- ارسال **پست‌های معمولی** (عکس، ویدیو، فایل) به کانال تلگرام
- ارسال **محصولات فروشگاهی** با فرمت حرفه‌ای و قیمت‌گذاری
- استفاده از **هوش مصنوعی Gemini گوگل** برای تولید خودکار کپشن جذاب
- **زمان‌بندی انتشار** مطالب
- **پنل مدیریت** کامل برای نظارت بر وضعیت ارسال‌ها

### 🚀 امکانات کلیدی

| ویژگی | توضیح |
|-------|-------|
| 🤖 هوش مصنوعی | تولید خودکار کپشن حرفه‌ای با Gemini AI |
| ⏰ زمان‌بندی | تعیین زمان دقیق انتشار پست‌ها و محصولات |
| 📊 داشبورد | مدیریت متمرکز تمام محتواها |
| 🖼️ پیش‌نمایش | مشاهده محصول قبل از ارسال نهایی |
| 🔐 احراز هویت | سیستم لاگین و خروج امن |
| 📱 ریسپانسیو | قابلیت استفاده در موبایل و دسکتاپ |

### 🛠️ تکنولوژی‌های استفاده شده

- **Backend**: Django 4.1
- **Database**: SQLite (قابل ارتقا به PostgreSQL)
- **Telegram API**: python-telegram-bot
- **AI**: Google Gemini AI (google-genai)
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Environment**: python-dotenv, django-environ

### 📁 ساختار پروژه
telegram_uploader_pro/
├── manage.py
├── telegram_uploader_pro/
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── uploader/
│ ├── models.py # مدل‌های Post و Product
│ ├── views.py # منطق اصلی برنامه
│ ├── utils.py # ارسال به تلگرام و AI
│ ├── tasks.py # تسک زمان‌بندی
│ └── templates/ # فایل‌های HTML
├── media/ # فایل‌های آپلودی
├── static/ # فایل‌های استاتیک
└── .env # متغیرهای محیطی

text

### 🔧 نصب و راه‌اندازی

#### پیش‌نیازها
- Python 3.9 یا بالاتر
- pip
- یک ربات تلگرام با توکن معتبر
- API Key سرویس Gemini گوگل

#### مراحل نصب

```bash
# 1. کلون کردن پروژه
git clone https://github.com/yourusername/telegram_uploader_pro.git
cd telegram_uploader_pro

# 2. ایجاد محیط مجازی
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. نصب وابستگی‌ها
pip install -r requirements.txt

# 4. تنظیم متغیرهای محیطی
cp .env.example .env
# ویرایش فایل .env با اطلاعات واقعی

# 5. اعمال migration‌ها
python manage.py migrate

# 6. جمع‌آوری فایل‌های استاتیک
python manage.py collectstatic

# 7. ایجاد کاربر ادمین
python manage.py createsuperuser

# 8. اجرای سرور
python manage.py runserver
⚙️ تنظیمات فایل .env
env
BOT_TOKEN=توکن_ربات_تلگرام_خود_را_وارد_کنید
CHANNEL_ID=@ایدی_کانال_مقصد
GEMINI_API_KEY=کلید_سرویس_جمینای_گوگل
📱 نحوه استفاده
وارد پنل مدیریت یا داشبورد شوید (/login)

برای ارسال پست معمولی به upload-post/ بروید

برای ارسال محصول به upload-product/ بروید

اطلاعات را وارد کرده و پیش‌نمایش را ببینید

در صورت تأیید، محصول به تلگرام ارسال می‌شود

پست‌های زمان‌بندی شده به صورت خودکار در زمان مقرر ارسال می‌شوند
👨‍💻 توسعه‌دهنده
فریبرز زمانی
📧 fariborz499@gmail.com