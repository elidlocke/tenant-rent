from .utility import timeStampToDate
from json import loads
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch


class Receipt():
    """ A receipt for a monthly rent payment

    Args:
        rentalInfo (dict): information about the property
        month (str): A string like 'January 2018'
        amount (int): The dollar amount of rent paid
        tenantName (str): Name of the tenant who has paid
        style (dict): collection of text formatting styles

    """

    def __init__(self,
                 rentalInfo,
                 room_id,
                 month,
                 amount,
                 tenantName):
        self.rentalInfo = rentalInfo
        self.room_id = room_id
        self.month = month
        self.amount = amount
        self.tenantName = tenantName
        self.style = self._createStyles()

    def _makeParagraph(self, text, paragraphStyleName):
        """ Create a single paragraph to add to the PDF doc"""
        p = Paragraph(
            text,
            self.style[paragraphStyleName]
        )
        return p

    def _createStyles(self):
        """ Add custom styles to stylesheet """
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

    def _addHeader(self):
        """ Header elements for receipt """

        h1 = Paragraph("<b>{}</b>".format(self.rentalInfo['propertyName']),
                       self.style['receiptTop'])
        h2 = Paragraph("Rental Reciept for {}"
                       .format(self.month.capitalize()),
                       self.style['receiptContent'])
        hr = HRFlowable(width="100%")
        return [h1, h2, Spacer(1, 4), hr, Spacer(1, 10)]

    def _addMidContent(self):
        """ Body elements for receipt """

        elements = []
        content = [("Address of Rental Unit:", "<br />"
                    .join(self.rentalInfo['address'])),
                   ("Month:", self.month),
                   ("Amount Paid:", "${}.00".format(self.amount)),
                   ("Recieved From:", self.tenantName),
                   ("Issued By:", self.rentalInfo['company'])]
        for item in content:
            head = self._makeParagraph(
                "<b>{}</b>".format(item[0]), 'receiptHeader')
            text = self._makeParagraph(item[1], 'receiptContent')
            elements.extend([head, text, Spacer(1, 12)])
        return elements

    def _addFooter(self, image_fd):
        """ Footer elements for receipt """

        footer = self._makeParagraph("For all questions contact {} at {}"
                                     .format(self.rentalInfo['landlord'],
                                             self.rentalInfo['phone']),
                                     'receiptContent')
        im = Image(image_fd, 1 * inch, 0.45 * inch)
        im.hAlign = 'LEFT'
        hr = HRFlowable(width="100%")
        return [im, Spacer(1, 4), hr, Spacer(1, 8), footer]

    def createPDF(self):
        """ Builds a story and creates a PDF File """
        monthStr = timeStampToDate(self.month)
        filename = "./app/receipts/receipt-{}-{}.pdf".format(
            self.tenantName.replace(" ", "-").lower(),
            monthStr.replace(" ", "-").lower())
        story = []
        doc = SimpleDocTemplate(
            filename,
            pagesize=(4 * inch, 5 * inch),
            rightMargin=15, leftMargin=15,
            topMargin=15, bottomMargin=15
        )
        image_path = "./app/resources/{}"\
                     .format(self.rentalInfo['signature'])
        with open(image_path, 'rb') as image_fd:
            story.extend(self._addHeader())
            story.extend(self._addMidContent())
            story.extend(self._addFooter(image_fd))
            doc.build(story)


def writeReceipts(db):
    sql_query = """SELECT tenants.name, rent.room_id, rent.date, rooms.price
                FROM rent
                INNER JOIN tenants ON tenants.user_id = rent.user_id
                INNER JOIN rooms ON rent.room_id = rooms.room_id
                WHERE rent.paid = 1 AND rent.receipt_issued = 0"""
    records = db.getQuery(sql_query)
    rental_fp = "./app/resources/rental.json"
    with open(rental_fp, 'r') as f:
        rentalInfo = loads(f.read())
    f.close()
    tenantNames = []
    for record in records:
        tenantNames.append(record[0])
        r = Receipt(rentalInfo,
                    room_id=record[1],
                    month=record[2],
                    amount=record[3],
                    tenantName=record[0])
        r.createPDF()
    update_sql = """UPDATE rent
                 SET receipt_issued = 1
                 WHERE paid = 1"""
    db.updateQuery(update_sql)
    return (list(set(tenantNames)))
