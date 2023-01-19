#!/usr/bin/python3

#Send Emails
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import logging

logging.basicConfig(filename='emailDKPlastics.log', filemode='a', format='%(asctime)s - %(name)s -  %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)


def sendEmail(messages='', lname='', fname=''):
    # Set test to 1 when testing
    body = f'There have been some differences in applications found.<br><br> {messages}'

    subject = f'Job application from {fname} {lname}'
    test = 1
    if test == 0:
        mypeople = ['cduhn@hotmail.com', 'brianhenry75@yahoo.com', 'cduhn75@gmail.com']

    else:
         mypeople = ['cduhn@hotmail.com', 'cduhn75@gmail.com']

    for person in mypeople:
        print(person)
        sender = 'no-reply@dkplastics.com'
        receivers = [f'{person}']
        mail = smtplib.SMTP()
        mail.connect('localhost')
        message = MIMEMultipart("alternative")
        message['From'] = 'DKPlastics Admin no-reply <no-reply@dkplastics.com>'
        message['To'] = f'{person}'
        message['Subject'] = f'{subject}'

        body1 = f'{body}'

        pdf = MIMEApplication(open(f"{fname}_jobapplication.pdf", 'rb').read())
        pdf.add_header('Content-Disposition', 'attachment',
                       filename=f"{fname}_jobapplication.pdf")
        message.attach(pdf)


        part1 = MIMEText(body1, "html")

        message.attach(part1)

        try:
            smtpObj = smtplib.SMTP('localhost')
            smtpObj.ehlo()
            smtpObj.sendmail(sender, receivers, message.as_string())
            logging.info(f"The job application for {fname}{lname} was sent successfully {subject}")
            print("Successfully sent email")
        except smtplib.SMTPException:

            logging.error(f'Exception occured ', exc_info=True)
            # print(f"Error: unable to send email{e}")

        except OSError as errorno:
            logging.error(f'The email did not send check to see if mail relay IP address is correct. {errorno}')




def main():

    sendEmail('Hi Brian This is a test.', 'duhn', 'craig')


if __name__ == '__main__':
    main()
