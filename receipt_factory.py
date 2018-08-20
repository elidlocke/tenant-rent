from manage_db import rentalDatabase
from receipt import receipt

buildingInfo = {
    "name": "Quarrie House",
    "address": ["54 Grand Ave N",
           "Cambridge, ON, Canada",
           "N1S 2K9"],
    "company": "2535057 Ontario Inc",
    "landlord": "Ben Locke",
    "phone": "519 721-2776",
    "signature": "./resources/signature.png"
}

def batchGenerateReceipts(db, mo_year):
    records = db.getOccupiedStatusByMonth(mo_year)
    tenantReceiptList = []
    for record in records:
        if record.rent_paid and not record.receipt_issued:
            r = receipt(buildingInfo['name'],
                        buildingInfo['address'],
                        buildingInfo['company'],
                        buildingInfo['landlord'],
                        buildingInfo['phone'],
                        buildingInfo['signature'],
                        mo_year,
                        record.room_price,
                        record.tenant_name)
            r.createPDF()
            tenantReceiptList.append((record.tenant_id, record.tenant_name))
    return (tenantReceiptList)

if __name__ == '__main__':
    db = rentalDatabase()
    batchGenerateReceipts(db, 'September 2018')
