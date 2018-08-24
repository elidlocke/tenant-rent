import unittest
from app.utils import monthToNumStr, dateToTimeStamp, timeStampToDate
from app.utils import termLookup, concatStrings


class TestUtils(unittest.TestCase):

    def test_monthToNumStr(self):
        self.assertEqual(monthToNumStr('january'), '01')
        self.assertEqual(monthToNumStr('fall'), '09')

    def test_dateToTimeStamp(self):
        self.assertEqual(dateToTimeStamp('March 2020'), '2020-03-01 00:00:00')

    def test_timeStampToDate(self):
        self.assertEqual(timeStampToDate('2020-03-01 00:00:00'), 'March 2020')

    def test_termLookup(self):
        self.assertEqual(termLookup('Winter 2019'),
                         ['2019-01-01 00:00:00',
                          '2019-02-01 00:00:00',
                          '2019-03-01 00:00:00',
                          '2019-04-01 00:00:00'])

    def test_concatStrings(self):
        self.assertEqual(concatStrings(['a']), 'a')
        self.assertEqual(concatStrings(['a', 'b']), 'a and b')
        self.assertEqual(concatStrings(['a', 'b', 'c']), 'a, b and c')
