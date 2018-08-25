import unittest
import io
import sys
from app.rentalDatabase import rentalDatabase


class TestRentalDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = rentalDatabase()

    def test_printQuery(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        TestRentalDatabase.db.printQuery(
            """SELECT user_id, name, email FROM tenants""")
        sys.stdout = sys.__stdout__
        printedWords = capturedOutput.getvalue().split()
        self.assertEqual(printedWords[0], 'user_id')
        self.assertEqual(printedWords[1], 'name')
        self.assertEqual(printedWords[2], 'email')

    def test_getQuery(self):
        result = self.db.getQuery(
            """ SELECT rooms.room_id
            FROM rooms
            WHERE rooms.rentable = 1""")
        available_rooms = ', '.join([item[0] for item in list(result)])
        self.assertEqual(available_rooms, 'A, D, E, F, G, H, I, J, K')
