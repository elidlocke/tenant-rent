import unittest
import os

from json import loads
from pathlib import Path
from app.writeReceipts import Receipt


class TestWriteReceipts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        file_path = 'app/resources/rental.json'
        with open(file_path, 'r') as f:
            rentalInfo = loads(f.read())
        f.close()
        print(rentalInfo['landlord'])
        cls.r = Receipt(rentalInfo, 'February 1000',
                        595, 'Joe Future')

    def test_writeReceipt(self):
        TestWriteReceipts.r.createPDF()
        testPath = Path("app/receipts/receipt-joe-future-february-1000.pdf")
        self.assertEqual(testPath.is_file(), True)
        if os.path.exists(testPath):
            os.remove(testPath)

    def test_writeReceipts(self):
        pass
