import unittest
from os import environ
from collections import namedtuple
from app.tenantEmail import tenantEmail


class TestTenantEmail(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        RentRecord = namedtuple('RentRecord',
                                ['tenant_id',
                                 'tenant_name',
                                 'tenant_email',
                                 'room_id',
                                 'date',
                                 'room_price',
                                 'rent_paid',
                                 'receipt_issued'])
        myRecord = RentRecord(1, 'may smith', 'bethnenniger+test@gmail.com',
                              'A', '2018-09-01 00:  00:00', 595, 1, 1)
        cls.e = tenantEmail(myRecord)

    def test_envVariables(self):
        self.assertEqual(isinstance(environ['SCRIPT_MAIL'], str), True)
        self.assertEqual(isinstance(environ['SCRIPT_PASSWORD'], str), True)

    def test_createMessage(self):
        TestTenantEmail.e._createMessage()
        self.assertEqual(self.e.message['To'], 'bethnenniger+test@gmail.com')
