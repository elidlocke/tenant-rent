def monthToNumStr(month):
    month_dict = {'january': '01', 'february': '02', 'march': '03',
                  'april': '04', 'may': '05', 'june': '06', 'july': '07',
                  'august': '08', 'september': '09', 'october': '10',
                  'november': '11', 'december': '12', 'winter': '01', 'summer': '05', 'fall': '09' }
    return month_dict[month.lower()]

def dateToTimeStamp(mm_yyyy):
    '''
    Take in a date like January 2018 and convert to a string timestamp
    '''
    date_info = mm_yyyy.split(' ')
    date = "{}-{}-01 00:00:00".format(date_info[1], monthToNumStr(date_info[0].lower()))
    return date

def termLookup(term):
    '''
    Take in a term, eg. winter 2019 and return dates for the four months
    for the term
    '''
    term_info = term.split(' ')
    term_dict = {'winter': ['01', '02', '03', '04'],
                 'summer': ['05', '06', '07', '08'],
                 'fall': ['09', '10', '11', '12']}
   
    dates = []
    for i in range(0,4):
        date = "{}-{}-01 00:00:00".format(term_info[1],
                term_dict[term_info[0].lower()][i])
        dates.append(date)
    return dates
