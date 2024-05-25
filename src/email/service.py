import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader


def send_html_email(user_email, user_name):
    from_address = "your_email@gmail.com"
    to_address = user_email
    message = MIMEMultipart("alternative")
    message["From"] = from_address
    message["To"] = to_address
    message["Subject"] = "Success Registration"

    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("email_template.html")
    html = template.render(name=user_name)

    part = MIMEText(html, "html")
    message.attach(part)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(from_address, "your_password")
    text = message.as_string()
    server.sendmail(from_address, to_address, text)
    server.quit()


# Call the function with the user's email and name
send_html_email("user_email@example.com", "John Doe")
