from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph,\
Spacer, Image
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, inch


class receipt():
    def __init__(self,
                 propertyName,
                 address,
                 company,
                 landlordName,
                 phone,
                 signature,
                 month,
                 amount,
                 tenantName):
        self.propertyName = propertyName
        self.address = address
        self.company = company
        self.landlordName = landlordName
        self.phone = phone
        self.signature = signature
        self.month = month
        self.amount = amount
        self.tenantName = tenantName
        self.style = self.createStyles()


    def makeParagraph(self, text, paragraphStyleName):
        p = Paragraph(
            text,
            self.style[paragraphStyleName]
        )
        return p

    def createStyles(self):
        style = getSampleStyleSheet()
        style.add(ParagraphStyle(name='receiptTop',
                                  fontSize=20,
                                  leading=24,
                                  trailing=24,
                                  fontName='Helvetica',
                                  textColor='#282828'))
        style.add(ParagraphStyle(name='receiptHeader',
                                  fontSize=10,
                                  leading=12,
                                  trailing=12,
                                  fontName='Helvetica',
                                  textColor='#282828'))
        style.add(ParagraphStyle(name='receiptContent',
                                  fontSize=10,
                                  leading=12,
                                  trailing=24,
                                  fontName='Helvetica',
                                  textColor='#666666'))
        return style

    def addHeader(self):
        h1 = Paragraph("<b>{}</b>".format(self.propertyName), self.style['receiptTop'])
        h2 = Paragraph("Rental Reciept for {}".format(self.month),
                        self.style['receiptContent'])
        hr = HRFlowable(width="100%")
        return [h1, h2, Spacer(1, 4), hr, Spacer(1, 10)]

    def addMidContent(self):
        elements = []
        content = [("Address of Rental Unit:", "<br />".join(self.address)),
                   ("Month:", self.month),
                   ("Amount Paid:", "${}.00".format(self.amount)),
                   ("Recieved From:", self.tenantName),
                   ("Issued By:", self.company)]
        for item in content:
            head = self.makeParagraph("<b>{}</b>".format(item[0]), 'receiptHeader')
            text = self.makeParagraph(item[1], 'receiptContent')
            elements.extend([head, text, Spacer(1, 12)])
        return elements

    def addFooter(self):
        footer = self.makeParagraph("For all questions contact {} at {}"\
                                .format(self.landlordName,
                                        self.phone), 
                                        'receiptContent')
        im = Image(self.signature, 1*inch, 0.45*inch)
        im.hAlign = 'LEFT'
        hr = HRFlowable(width="100%")
        return [im, Spacer(1, 4), hr, Spacer(1, 8), footer]

    def createPDF(self):
        filename = "receipts/receipt-{}-{}.pdf".format(
                self.tenantName.replace(" ","-").lower(),
                self.month.replace(" ", "-").lower())
        story = []
        doc = SimpleDocTemplate(
            filename,
            pagesize=(4*inch, 5*inch),
            rightMargin=15,leftMargin=15,
            topMargin=15,bottomMargin=15
        )
        story.extend(self.addHeader())
        story.extend(self.addMidContent())
        story.extend(self.addFooter())
        doc.build(story)


if __name__ == '__main__':
    propertyName = "Quarrie House"
    address = ["54 Grand Ave N", "Cambridge, ON, Canada", "N1S 2K9"]
    company = "2535057 Ontario Inc"
    landlordName = "Ben Locke"
    phone = "519 721-2776"
    signature = "./resources/signature.png"
    month = 'January 2018'
    amount = '595'
    tenantName = 'Salina Lee'

    rec = receipt(propertyName,
                 address,
                 company,
                 landlordName,
                 phone,
                 signature,
                 month,
                 amount,
                 tenantName)
    rec.createPDF()
