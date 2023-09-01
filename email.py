import win32com.client
import time
import os

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

# Define the list of companies and their respective email addresses
email_lists = {
    'TEST': [
        'benjamin.thompson1@ibm.com',
        'benjaminthompson.au@gmail.com',
    ],
    'AEC': [
        'Christine.Joy@aec.gov.au',
        'Mike.Nielsen@aec.gov.au','Sandy.Lambe@aec.gov.au'
    ],
    'ATO': [
        'Michael.Edmondson@ato.gov.au',
        'Michael.Wade@ato.gov.au',
        'Samir.Mathur@ato.gov.au',
        'Chandima.DeSilva@ato.gov.au',
        'Richard.Baker@ato.gov.au',
        'Sameer.Gaur@ato.gov.au',
        'Tony.Huynh@ato.gov.au',
        'Owen.Davies@ato.gov.au',
        'Lachlan.McKenzie@ato.gov.au',
        'Aaron.Draper@ato.gov.au',
        'Ben.Coffison@ato.gov.au',
        'Shane.Bazin@ato.gov.au',
        'Marta.Peemoeller@ato.gov.au',
        'John.Carter@ato.gov.au'
    ],
    'DFAT': [
        'Tony.O''Sullivan@dfat.gov.au',
        'Stephen.Yost@dfat.gov.au'
    ],
    'DXC': [
        'Stephen.Mallett@dxc.com',
        'rslater@dxc.com',
        'Sam.Arnold@ato.gov.au'
    ],
    'HomeAffairs': [
        'Aldred.Gonzalez@homeaffairs.gov.au',
        'Aaron.Tully@homeaffairs.gov.au',
        'Mark.Boddy@homeaffairs.gov.au',
        'Douglas.Lean@homeaffairs.gov.au',
        'Michael.Fawke@homeaffairs.gov.au',
        'Chris.Tullis@homeaffairs.gov.au',
        'Simon.Kneebone@homeaffairs.gov.au',
        'Luis.Monge@homeaffairs.gov.au'
    ],
    'NTG': [
        'andrew.krink@nt.gov.au',
        'Campbell.Marshall@nt.gov.au',
        'Shane.Harrison@nt.gov.au',
        'heath.dewson@nt.gov.au',
        'Patrick.Welsh@nt.gov.au',
        'Haydn.Russell@nt.gov.au',
        'Roger.Lowe@nt.gov.au',
        'John.Yorke-Barber@nt.gov.au',
        'Elina.Woolley@nt.gov.au',
        'Anthony.Thompson@nt.gov.au',
        'Patrick.yeung@nt.gov.au',
        'Ross.Maddock@nt.gov.au',
        'John.McAskill@nt.gov.au',
        'Elizabeth.Shenton@nt.gov.au',
        'aaron.hay@nt.gov.au',
        'Tina.Sacca@nt.gov.au',
        'Angelito.Lontoc@nt.gov.au',
        'Harita.Lingamaneni@nt.gov.au',
        'Gilbert.Simpkins@nt.gov.au',
        'Chai.Barretto@nt.gov.au',
        'Julius.Marbella@nt.gov.au'
    ],
    'ServicesAustralia': [
        'rick.whittle@servicesaustralia.gov.au',
        'Graeme.Whitfield@servicesaustralia.gov.au',
        'Glenda.Coffey@servicesaustralia.gov.au',
        'Steffen.Moebus@servicesaustralia.gov.au',
        'Peter.Daley@servicesaustralia.gov.au',
        'Gary.Allardyce@servicesaustralia.gov.au',
        'tariq.tarbuck2@servicesaustralia.gov.au',
        'sharon.grant2@servicesaustralia.gov.au',
        'Goff.Cureton@servicesaustralia.gov.au',
        'kylie.miles@servicesaustralia.gov.au',
        'Alan.Smith@servicesaustralia.gov.au',
        'Graham.Achilles@servicesaustralia.gov.au',
        'Glenda.Ozolins@servicesaustralia.gov.au',
        'Sadaf.Irfan@servicesaustralia.gov.au>',
        'peter.cottrell@servicesaustralia.gov.au',
        'Clayton.Mumford@servicesaustralia.gov.au',
        'Robert.Mills@servicesaustralia.gov.au',
        'Craig.mckellar2@servicesaustralia.gov.au',
        'frank.wallace@servicesaustralia.gov.au',
        'ted.hempstead@servicesaustralia.gov.au'
    ],
    'ISI': [
        'Josh.Stewart@isi.com.au',
        'MikeU@isi.com.au',
        'Lindsay.Oxenham@isi.com.au',
        'john.hosking@isi.com.au',
        'Mladen.Ervacanin@isi.com.au',
        'Nenad.Vasiljevic@isi.com.au',
        'josh.cukurins@defence.gov.au'
    ],
    'IBM':[
        'pgovend@au1.ibm.com',
        'iannobbs@au1.ibm.com',
        'Thanh.N@ibm.com',
        'jaysen@au1.ibm.com',
        'graeme.muddle@au1.ibm.com'
    ],
    # add more companies and emails as needed
}

# Define the subject and body of the email
subject = 'September 2023 Webinar Calendar: z/OS Academy APAC Edition'
body = '''
{additional_text}
Good morning,
We are excited to share the calendar for the upcoming z/OS Academy APAC Edition webinars in September 2023. This month, we have four live presentations that we believe will provide valuable insights and knowledge to you and your team.

Please share this information with your teammates and others interested in IBM System Z.

Additionally, detailed information about the webinars, including the topics, speakers, and registration links, can be found in the attached PDF September 2023 newsletter.

Thank you for your continued support and engagement with the IBM Z community.

Best Regards,

Ben Thompson
Advisory zStack Client Architect
Phone: 0439 032 104
E-mail: benjamin.thompson1@ibm.com
'''
# Define the list of attachments
attachments = ['C:\\Users\\ZZ02Z5616\\Downloads\\zOS Academy newsletter 2023 - Sep.pdf']

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