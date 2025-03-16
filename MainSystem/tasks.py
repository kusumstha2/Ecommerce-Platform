# # from celery import shared_task

# # @shared_task
# # def my_background_task():
# #     print("Task is running!")
# #     return "Task completed!"

# # base/tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

@shared_task
def send_package_email(user_id, package_name, price, duration, expiry_date):
    User = get_user_model()
    user = User.objects.get(id=user_id)

    subject = "Package Purchase Confirmation"
    message = f"""
    Dear {user.username},

    Thank you for purchasing the '{package_name}' package!

    Your package details:
    - Package Name: {package_name}
    - Price: ${price}
    - Duration: {duration}
    - Expiry Date: {expiry_date}

    You can now access your package features.

    Best Regards,  
    Mindriser Tech
    """

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        # "ujjwalneupane01@gmail.com",
        fail_silently=True,
    )
    return "Email sent"

# from celery import shared_task
# from django.core.mail import send_mail
# from django.conf import settings

# @shared_task
# def send_test_email():
#     subject = "Celery Test Email"
#     message = "This is a test email to confirm Celery is working."
#     recipient_list = ["ujjwalneupane01@gmail.com"]

#     send_mail(
#         subject,
#         message,
#         settings.DEFAULT_FROM_EMAIL,
#         recipient_list,
#         fail_silently=False,
#     )

#     return "Test email sent successfully!"
