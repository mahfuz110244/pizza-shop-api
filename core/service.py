from django.core.mail import EmailMessage
# import the logging library
import logging
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.core.cache import cache

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Modified version of a GIST I found in a SO thread
class CachingPaginator(Paginator):
    def _get_count(self):

        if not hasattr(self, "_count"):
            self._count = None

        if self._count is None:
            try:
                key = "adm:{0}:count".format(hash(self.object_list.query.__str__()))
                self._count = cache.get(key, -1)
                if self._count == -1:
                    self._count = super().count
                    cache.set(key, self._count, 3600)

            except:
                self._count = len(self.object_list)
        return self._count

    count = property(_get_count)


def custom_response(success, status_code, data=None, headers=None, error=None, errorMessage=None):
    """
    This is Custom Return Response Handler
    :param success:
    :param status_code:
    :param data:
    :param headers:
    :param error:
    :param errorMessage:
    :return:
    """
    if not success:
        error = {'errorCode': status_code, 'errorMessage': errorMessage}
    response = {'success': success, 'status_code': status_code, 'data': data, 'error': error}
    return Response(response, status=status_code, headers=headers)


# Send EMAIL
def mail_send(email_to, subject, message, from_email):
    # Try to send the message.
    try:
        email = EmailMessage()
        email.subject = subject
        email.body = message
        email.from_email = from_email
        email.to = [email_to, ]
        email.send()
        logger.info("Email send")
        return True
        # Display an error message if something goes wrong.
    except Exception as e:
        logger.error("Error: ", e)
        return False


def mail_send_with_file(email_to, subject, message, from_email, filename):
    # Try to send the message.
    try:
        email = EmailMessage()
        email.subject = subject
        email.body = message
        email.from_email = from_email
        email.to = [email_to, ]

        # email.attach_file(filename)  # Attach a file directly

        # Or alternatively, if you want to attach the contents directly

        file = open(filename, "rb")
        email.attach(filename=filename, mimetype="application/pdf", content=file.read())
        file.close()

        email.send()
        logger.info("Email send")
        return True
        # Display an error message if something goes wrong.
    except Exception as e:
        logger.error("Error: ", e)
        return False


# Send Email Via AWS SNS
def aws_sharing_mail_send(email_to, message):
    import smtplib
    import email.utils
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    # Replace sender@example.com with your "From" address.
    # This address must be verified.
    SENDER = 'revera420@gmail.com'
    SENDERNAME = 'Revera'

    # Replace recipient@example.com with a "To" address. If your account
    # is still in the sandbox, this address must be verified.
    RECIPIENT = email_to

    # Replace smtp_username with your Amazon SES SMTP user name.
    USERNAME_SMTP = "AKIAJBV5VNO5KVASPSMQ"

    # Replace smtp_password with your Amazon SES SMTP password.
    PASSWORD_SMTP = "AnZh6ow8pJ3oU6YqHKit7gVAZ2lt2ra/9J9BmNhq1Xmu"

    # (Optional) the name of a configuration set to use for this message.
    # If you comment out this line, you also need to remove or comment out
    # the "X-SES-CONFIGURATION-SET:" header below.
    # CONFIGURATION_SET = "ConfigSet"

    # If you're using Amazon SES in an AWS Region other than US West (Oregon),
    # replace email-smtp.us-west-2.amazonaws.com with the Amazon SES SMTP
    # endpoint in the appropriate region.
    HOST = "email-smtp.eu-west-1.amazonaws.com"
    PORT = 587

    # The subject line of the email.
    SUBJECT = 'OTP from Revera Heath App'

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = (message)

    # The HTML body of the email.
    BODY_HTML = message

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
    msg['To'] = RECIPIENT
    # Comment or delete the next line if you are not using a configuration set
    # msg.add_header('X-SES-CONFIGURATION-SET', CONFIGURATION_SET)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(BODY_TEXT, 'plain')
    part2 = MIMEText(BODY_HTML, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Try to send the message.
    try:
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        server.starttls()
        # stmplib docs recommend calling ehlo() before & after starttls()
        server.ehlo()
        server.login(USERNAME_SMTP, PASSWORD_SMTP)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())
        server.close()
    # Display an error message if something goes wrong.
    except Exception as e:
        print("Error: ", e)
        return False
    else:
        print("Email sent!")
        return True
