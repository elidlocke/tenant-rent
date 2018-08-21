import os
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from helper_functions import timeStampToDate

class tenantEmail():
    def __init__(self, rentRecord):
        self.message = MIMEMultipart()
        self.rentRecord = rentRecord
        self.senderEmail = os.environ['SCRIPT_MAIL']
        self.senderPass = os.environ['SCRIPT_PASSWORD']

    def createSubject(self):
        if self.rentRecord.rent_paid == True:
            subjectText = "Rent Receipt"
        else:
            subjectText = "Rent Reminder"
        return ("{} {}".format(timeStampToDate(self.rentRecord.date),
                               subjectText))

    def createMessage(self):
        self.message['From'] = self.senderEmail
        self.message['To'] = str(self.rentRecord.tenant_email)
        self.message['Subject'] = self.createSubject()

    def addBodyText(self):
        if self.rentRecord.rent_paid == True:
            bodyText = "<html>Hi {},<br>Attached is your receipt for {}</html>"\
                    .format(self.rentRecord.tenant_name.title(),
                            timeStampToDate(self.rentRecord.date))
        else:
            bodyText = "<html>Hi {}, Your rent for {} is due.\
            Please provide us with a cheque or e-transfer for {} ASAP. </html>"\
            .format(self.rentRecord.tenant_name.title(),
                    timeStampToDate(self.rentRecord.date),
                    self.rentRecord.room_price)
        self.message.attach(MIMEText(bodyText,'html'))

    def addPDF(self):
        filepath = "./receipts/receipt-{}-{}.pdf"\
               .format(
               self.rentRecord.tenant_name.replace(" ", "-").lower(),
               timeStampToDate(self.rentRecord.date).replace(" ","-").lower())
        fp=open(filepath,'rb')
        att = MIMEApplication(fp.read(),_subtype="pdf")
        fp.close()
        att.add_header('Content-Disposition','attachment',filename='receipt.pdf')
        self.message.attach(att)

    def send(self):
        self.createSubject()
        self.createMessage()
        self.addBodyText()
        self.addPDF()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.connect('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.senderEmail, self.senderPass)
        server.send_message(self.message)
        server.quit()

if __name__ == '__main__':
    from collections import namedtuple
    RentRecord = namedtuple('RentRecord',
                         ['tenant_id',
                          'tenant_name',
                          'tenant_email',
                          'room_id',
                          'date',
                          'room_price',
                          'rent_paid',
                          'receipt_issued'])
    myRecord = RentRecord(1, 'may smith', 'bethnenniger@gmail.com', 'A', '2018-09-01 00:00:00', 595, 1, 1)
    e = tenantEmail(myRecord)
    e.send()
