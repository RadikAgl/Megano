import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from uuid import uuid4
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.urls import reverse


def mail(recipient_email, random_number):
    uuid = uuid4()
    smtp_server = 'smtp.yandex.ru'
    smtp_port = 465
    smtp_username = 'kudakaevnikita@yandex.ru'
    smtp_password = 'smoskarjxbcwezdj'

    # Sender and recipient email addresses
    sender_email = 'kudakaevnikita@yandex.ru'
    recipient_email = f'{recipient_email}'

    # Пользователь, для которого нужно сгенерировать токен
    user = get_user_model().objects.get(email=recipient_email)

    # Генерация токена сброса пароля для пользователя
    token = default_token_generator.make_token(user)
    reset_url = reverse('user:reset_password_confirm', kwargs={'uidb64': uuid, 'token': token})
    # Email content
    subject = 'shop Megano'

    body = f"""
<html>
<head></head>
<body>
    <p>Привет: vazaxac@gmail.com, если вы хотите изменить пароль, <a href={'http://127.0.0.1:8000' + reset_url}
     title='сброс'>нажмите тут</a>. ваш код {random_number}</p>
</body>
</html>
"""

    # Create MIME message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'html'))

    try:
        # Establish a connection to the SMTP server
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            # Log in to the SMTP server using app password
            server.login(smtp_username, smtp_password)

            # Send the email
            server.sendmail(sender_email, recipient_email, message.as_string())

        print('Email sent successfully!')

    except Exception as e:
        print(f'Error: {e}')
    return token
