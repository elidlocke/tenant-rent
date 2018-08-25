def monthToNumStr(month):
    """Convert a month from a string of letters to  a string of digits"""

    month_dict = {'january': '01', 'february': '02', 'march': '03',
                  'april': '04', 'may': '05', 'june': '06', 'july': '07',
                  'august': '08', 'september': '09', 'october': '10',
                  'november': '11', 'december': '12', 'winter': '01',
                  'summer': '05', 'fall': '09'}
    return month_dict[month.lower()]


def dateToTimeStamp(mm_yyyy):
    """Convert a date like 'January 2018' to a string timestamp"""

    date_info = mm_yyyy.split(' ')
    date = "{}-{}-01 00:00:00".format(date_info[1],
                                      monthToNumStr(date_info[0].lower()))
    return date


def timeStampToDate(timestamp):
    """Convert a string timestamp to a string in the format 'Month Year'. """

    month_dict = {'01': 'january', '02': 'february', '03': 'march',
                  '04': 'april', '05': 'may', '06': 'june', '07': 'july',
                  '08': 'august', '09': 'september', '10': 'october',
                  '11': 'november', '12': 'december'}
    month = month_dict[timestamp[5:7]].capitalize()
    year = timestamp[:4]
    timeString = "{} {}".format(month, year)
    return timeString


def termLookup(term):
    """Return the corresponding timestamps for a school term"""

    term_info = term.split(' ')
    term_dict = {'winter': ['01', '02', '03', '04'],
                 'summer': ['05', '06', '07', '08'],
                 'fall': ['09', '10', '11', '12']}
    dates = []
    for i in range(0, 4):
        date = "{}-{}-01 00:00:00".format(term_info[1],
                                          term_dict[term_info[0].lower()][i])
        dates.append(date)
    return dates


def concatStrings(words):
    """Format an array of words nicely for printing in a sentance"""

    printWords = None
    if len(words) > 2:
        printWords = ', '.join(words[:-1]) + ' and ' + str(words[-1])
    elif len(words) == 2:
        printWords = ' and '.join(words)
    elif len(words) == 1:
        printWords = words[0]
    return printWords
