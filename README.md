🇬🇧 <span id="en">English Version</span>
📌 Project Overview
Telegram Uploader Pro is a web application built with Django that enables you to:

Send regular posts (photos, videos, files) to Telegram channels

Send shop products with professional formatting and pricing

Use Google Gemini AI for automatic caption generation

Schedule content for future publishing

Monitor everything through a complete admin panel

🚀 Key Features
Feature	Description
🤖 AI Integration	Auto-generate professional captions with Gemini AI
⏰ Scheduling	Set exact publish time for posts and products
📊 Dashboard	Centralized content management
🖼️ Preview	Preview products before final send
🔐 Authentication	Secure login/logout system
📱 Responsive	Works on mobile and desktop
🛠️ Technologies
Backend: Django 4.1

Database: SQLite (upgradable to PostgreSQL)

Telegram API: python-telegram-bot

AI: Google Gemini AI (google-genai)

Frontend: HTML5, CSS3, Bootstrap 5

Environment: python-dotenv, django-environ

📁 Project Structure
text
telegram_uploader_pro/
├── manage.py
├── telegram_uploader_pro/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── uploader/
│   ├── models.py      # Post & Product models
│   ├── views.py       # Main application logic
│   ├── utils.py       # Telegram & AI integration
│   ├── tasks.py       # Scheduled tasks
│   └── templates/     # HTML files
├── media/             # Uploaded files
├── static/            # Static files
└── .env               # Environment variables
🔧 Installation
Prerequisites
Python 3.9 or higher

pip

Telegram bot with valid token

Google Gemini API Key

Setup Steps
bash
# 1. Clone repository
git clone https://github.com/yourusername/telegram_uploader_pro.git
cd telegram_uploader_pro

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 5. Run migrations
python manage.py migrate

# 6. Collect static files
python manage.py collectstatic

# 7. Create admin user
python manage.py createsuperuser

# 8. Start server
python manage.py runserver
⚙️ .env Configuration
env
BOT_TOKEN=your_telegram_bot_token_here
CHANNEL_ID=@your_channel_username
GEMINI_API_KEY=your_google_gemini_api_key
📱 How to Use
Log in to Admin Panel or Dashboard (/login)

To send a regular post, go to upload-post/

To send a product, go to upload-product/

Enter details and check preview

Confirm to send to Telegram

Scheduled posts will be sent automatically at the set time

👨‍💻 Developer
Fariborz Zamani
📧 fariborz499@gmail.com

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🤝 Contributing
Contributions, issues, and feature requests are welcome!

<p align="center"> Made with ❤️ by Fariborz Zamani </p> ```