# uploader/apps.py
from django.apps import AppConfig

class UploaderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'uploader'

    def ready(self):
        # فقط تو حالت توسعه (runserver) اجرا بشه
        import os
        if os.environ.get('RUN_MAIN'):  # این خط مهمه!
            from .tasks import check_scheduled_items
            import threading
            threading.Thread(target=check_scheduled_items, daemon=True).start()