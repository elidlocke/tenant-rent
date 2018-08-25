import unittest
import app.utility as u


class TestUtils(unittest.TestCase):

    def test_monthToNumStr(self):
        self.assertEqual(u.monthToNumStr('january'), '01')
        self.assertEqual(u.monthToNumStr('fall'), '09')

    def test_dateToTimeStamp(self):
        self.assertEqual(u.dateToTimeStamp('March 2020'),
                         '2020-03-01 00:00:00')

    def test_timeStampToDate(self):
        self.assertEqual(u.timeStampToDate(
                    '2020-03-01 00:00:00'
        ), 'March 2020')

    def test_termLookup(self):
        self.assertEqual(u.termLookup('Winter 2019'),
                         ['2019-01-01 00:00:00',
                          '2019-02-01 00:00:00',
                          '2019-03-01 00:00:00',
                          '2019-04-01 00:00:00'])

    def test_concatStrings(self):
        self.assertEqual(u.concatStrings(['a']), 'a')
        self.assertEqual(u.concatStrings(['a', 'b']), 'a and b')
        self.assertEqual(u.concatStrings(['a', 'b', 'c']), 'a, b and c')
