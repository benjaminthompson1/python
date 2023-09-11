import win32com.client
import time
import os
import json

# Ask the user for the JSON file name/path and load the email lists
json_file_name = input("Please enter the JSON file name (or path) containing the email lists: ")
try:
    with open(json_file_name, 'r') as file:
        email_lists = json.load(file)
except FileNotFoundError as e:
    print(f"Could not find the JSON file: {e}")
    exit(1)
except json.JSONDecodeError as e:
    print(f"Failed to decode JSON file: {e}")
    exit(1)

# Define a function to send an email with optional attachments and a specified number of retries
def send_email(to, subject, body, company, attachments=None, retries=3):
    outlook = win32com.client.Dispatch('outlook.application')
    for recipient in to:
        for _ in range(retries):
            try:
                # Check if attachments exist and are valid files
                if attachments:
                    for attachment in attachments:
                        if not os.path.isfile(attachment):
                            raise FileNotFoundError(f"File not found: {attachment}")

                # Create email
                mail = outlook.CreateItem(0)
                mail.To = recipient
                mail.Subject = subject
                mail.Body = body
                if attachments:
                    for attachment in attachments:
                        mail.Attachments.Add(attachment)
                # Send email                        
                mail.Send()
                print(f"Email sent to {recipient} at {company}")
                time.sleep(5)  # 5 seconds delay to avoid sending too many emails too quickly
                break
            except Exception as e:
                print(f"An error occurred: {e}. Retrying...")
        else:
            raise Exception(f"Failed to send email to {recipient} after {retries} retries")

# Define the subject and body of the email
subject = 'Join us for the IBM Z Technical Team''s zSystems Forum Events - Face-to-Face in 6 Locations!'
body = '''
{additional_text}
Good afternoon,
We're thrilled to announce the return of the IBM Z Technical Team's zSystems Forum Events, taking place from October 2nd to October 13th, 2023, in 6 locations across Australia and ASEAN. This year, we're excited to host the events face-to-face, providing an excellent opportunity to connect with industry experts and like-minded professionals.

The event details are as follows:

* Dates: October 2nd - October 13th, 2023
* Locations: Sydney, Melbourne, Brisbane, Perth, Singapore, and Kuala Lumpur
* Event Type: Full-day event
* Session Tracks:
	1. Infrastructure
	2. Modernization: Data & AI
	3. DevOps and AIOps
* Number of Sessions: 16
* Registration: Please register for your chosen location and indicate your preferred stream.

To view the invitation and session details, click within the attachment.

We've designed this event to help organisations like yours modernize applications and enhance end-user experiences. Don't miss this opportunity to learn from industry experts, network with peers, and explore the latest solutions from IBM Z.

If you have any questions or need assistance with registration, please don't hesitate to reach out to me directly. Feel free to share this invitation with colleagues who may also benefit from attending.

We're looking forward to seeing you at one of our zSystems Forum Events!

Best regards,

Ben Thompson
Advisory zStack Client Architect
Phone: 0439 032 104
E-mail: benjamin.thompson1@ibm.com
'''
# Define the list of attachments
attachments = ['C:\\Users\\ZZ02Z5616\\Downloads\\IBM zForum October 2023 Invitation.pdf']

# Send a test email to 'TEST'
company = 'TEST'
additional_text = ''
company_subject = f"{company} - {subject}"
body = body.format(additional_text=additional_text)
try:
    send_email(email_lists[company], company_subject, body, company, attachments)
    print(f"Test email sent to {company}")
except Exception as e:
    print(f"An error occurred while sending test email to {company}: {e}")

# Ask the user if they want to send the emails to all companies
response = input("Are you satisfied with the test email and want to send emails to all companies? (yes/no): ")
if response.lower() == 'yes':
    for company, emails in email_lists.items():
        if company == 'TEST':  # skip the test company
            continue
        additional_text = ''
        if company == 'IBM':
            additional_text = 'Information only - the following email was sent to your account on IBM System Z education.'
        company_subject = f"{company} - {subject}"
        body = body.format(additional_text=additional_text)
        try:
            send_email(emails, company_subject, body, company, attachments)
            time.sleep(60) # 1 minutes delay to avoid sending too many emails too quickly
        except Exception as e:
            print(f"An error occurred while sending email to {company}: {e}")
            response = input("Do you want to continue to the next company? (yes/no): ")
            if response.lower() != 'yes':
                break