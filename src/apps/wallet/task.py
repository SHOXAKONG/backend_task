from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from src.apps.common.utils import code_generate
from src.apps.users.models import Code, User

@shared_task
def send_code_activate_wallet_task(to, user_id):
    try:
        user = User.objects.get(id=user_id)
        code = code_generate()
        Code.objects.create(code=code, user=user)

        subject = "Activate Wallet"
        from_email = "bekmurodovshohruh0224@gmail.com"
        recipient_list = [to]
        text_content = "Activate wallet"

        html_content = f"""
        <main>
            <h1>Hello, {user.email}!</h1>
            <h2>Activation Code: {code}</h2>
        </main>
        """

        email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
        email.attach_alternative(html_content, "text/html")
        email.send()
        print("Verification email sent!")
    except Exception as e:
        print(f"Error sending verification email: {e}")