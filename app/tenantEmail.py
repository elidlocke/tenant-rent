import smtplib

from os import environ
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from app.utils import timeStampToDate
from collections import namedtuple

class tenantEmail():
    """ Compose an email with a rent reciept or rent reminder for a tenant

    Attributes:
        message (MIMEMultipart): message to be sent
        rentRecord (namedtuple): tenant's information
        senderEmail (str): landlord's email
        senderPass (str): landlord's email password
    """
    def __init__(self, rentRecord):
        self.message = MIMEMultipart()
        self.rentRecord = rentRecord
        self.senderEmail = environ['SCRIPT_MAIL']
        self.senderPass = environ['SCRIPT_PASSWORD']

    def _createSubject(self):
        """ Create the email subject
        Returns:
            str: email subject
        """
        if self.rentRecord.rent_paid is True:
            subjectText = "Rent Receipt"
        else:
            subjectText = "Rent Reminder"
        return ("{} {}".format(timeStampToDate(self.rentRecord.date),
                               subjectText))

    def _createMessage(self):
        """ Create the informantion for the message itself """
        self.message['From'] = self.senderEmail
        self.message['To'] = str(self.rentRecord.tenant_email)
        self.message['Subject'] = self._createSubject()
        if self.rentRecord.rent_paid is True:
            bodyText = "<html>Hi {},\
                       <br>Attached is your receipt for {}</html>"\
                       .format(self.rentRecord.tenant_name.title(),
                               timeStampToDate(self.rentRecord.date))
        else:
            bodyText = "<html>Hi {}, Your rent for {} is due.\
            Please provide us with a cheque or e-transfer for {} ASAP. </html>"\
            .format(self.rentRecord.tenant_name.title(),
                    timeStampToDate(self.rentRecord.date),
                    self.rentRecord.room_price)
        self.message.attach(MIMEText(bodyText, 'html'))

    def _attachPDF(self):
        """ Attach the PDF receipt to the message """
        filepath = "./receipts/receipt-{}-{}.pdf"\
            .format(
                self.rentRecord.tenant_name.replace(" ", "-").lower(),
                timeStampToDate(self.rentRecord.date).replace(" ", "-").lower()
            )
        fp = open(filepath, 'rb')
        att = MIMEApplication(fp.read(), _subtype="pdf")
        fp.close()
        att.add_header('Content-Disposition',
                       'attachment',
                       filename='receipt.pdf')
        self.message.attach(att)

    def send(self):
        self.createSubject()
        self.createMessage()
        if self.rentRecord.rent_paid is True:
            self.attachPDF()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.connect('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.senderEmail, self.senderPass)
        server.send_message(self.message)
        server.quit()

def sendEmails(db):
    sql_query = """SELECT tenants.name, tenants.email,
                rent.date, rooms.price
                FROM rent
                INNER JOIN tenants
                ON rent.user_id = tenants.user_id
                INNER JOIN rooms
                ON rent.room_id = rooms.room_id
                WHERE rent.receipt_issued = 1 AND rent.paid = 1
                AND rent.receipt_sent = 0"""
    result = db.getQuery(sql_query)
    RentRecord = namedtuple('RentRecord',
                            ['tenant_name',
                             'tenant_email',
                             'date',
                             'room_price'])
    rentRecords = [RentRecord(*row) for row in result]
    peopleEmailed = []
    for record in rentRecords:
        e = tenantEmail(record)
        e.send()
        peopleEmailed.append(record.tenant_name)
    update_sql = "UPDATE rent SET receipt_sent = 1"
    db.updateQuery(update_sql)
    return (peopleEmailed)
