from django.urls import path

urlpatterns = [
    # فقط برای اینکه خطا نده
    path(
        "send-post/<int:post_id>/", lambda request, post_id: None, name="send_post_now"
    ),
    path(
        "send-product/<int:product_id>/",
        lambda request, product_id: None,
        name="send_product_now",
    ),
]
