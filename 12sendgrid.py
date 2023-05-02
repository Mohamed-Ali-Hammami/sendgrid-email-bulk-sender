import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.headerregistry import Address
from email.utils import formataddr
import os


# Get user input for email details
smtp_server = input("Enter SMTP server: ")
smtp_port = input("Enter SMTP port: ")
smtp_username = input("Enter SMTP username: ")
smtp_password = input("Enter SMTP password: ")
sender_email = input("Enter sender email: ")
recipient_list_file = input("Enter path to recipient list file: ")
email_subject = input("Enter email subject: ")
html_file_path = input("Enter path to HTML file: ")


def validate_recipient_list_file_path(recipient_list_file):
    if not recipient_list_file:
        print("ERROR: recipient_list_file path cannot be empty.")
        return False

    if not os.path.exists(recipient_list_file):
        print(f"ERROR: recipient_list_file {recipient_list_file} does not exist.")
        return False

    if not os.path.isfile(recipient_list_file):
        print(f"ERROR: {recipient_list_file} is not a file.")
        return False

    if not recipient_list_file.lower().endswith('.txt'):
        print(f"ERROR: {recipient_list_file} is not an txt file.")
        return False

    if "\\" in recipient_list_file:
        print(f"ERROR: HTML file path must use forward slashes instead of backslashes.")
        return False

    return True


def validate_html_file_path(html_file_path):
    if not html_file_path:
        print("ERROR: HTML file path cannot be empty.")
        return False

    if not os.path.exists(html_file_path):
        print(f"ERROR: HTML file path {html_file_path} does not exist.")
        return False

    if not os.path.isfile(html_file_path):
        print(f"ERROR: {html_file_path} is not a file.")
        return False

    if not html_file_path.lower().endswith('.html'):
        print(f"ERROR: {html_file_path} is not an HTML file.")
        return False

    if "\\" in html_file_path:
        print(f"ERROR: HTML file path must use forward slashes instead of backslashes.")
        return False

    return True



# Validate HTML file path
while not validate_html_file_path(html_file_path):
    html_file_path = input("Enter path to HTML file: ")

# Read the recipient list from file
while not validate_recipient_list_file_path(recipient_list_file):
    recipient_list_file = input("Enter path to recipient list file: ")

with open(recipient_list_file, 'r') as f:
    recipient_list = f.read().splitlines()

# Set up the email message
msg = MIMEMultipart()
msg['From'] = sender_email
msg['Subject'] = email_subject

# Read the HTML content from a file
with open(html_file_path, encoding='utf-8') as f:
    html_content = f.read()

# Attach the HTML content to the message
html_part = MIMEText(html_content, 'html')
msg.attach(html_part)

# Encode the sender email address
sender_name, sender_email = 'Your Name', sender_email
sender_address = Address(display_name=sender_name, username=sender_email.split('@')[0], domain=sender_email.split('@')[1])
msg['From'] = formataddr((sender_address.display_name, str(sender_address)))

# Set up the SMTP connection and send the email to each recipient
try:
    print("Setting up SMTP connection...")
    smime = smtplib.SMTP(smtp_server, smtp_port)
    smime.ehlo()
    smime.starttls()
    smime.ehlo()
    smime.login(smtp_username, smtp_password)
    print("SMTP connection established and logged in successfully.")
    
    for recipient_email in recipient_list:
        msg['To'] = recipient_email
        smime.sendmail(msg['From'], recipient_email, msg.as_string())
        print(f"Email sent successfully to {recipient_email}!")
    
    smime.quit()
    print("All emails sent successfully!")
except Exception as e:
    print("An error occurred while sending the emails:", e)

# Prompt the user to exit the program
print("Press Enter to exit...")
input()

