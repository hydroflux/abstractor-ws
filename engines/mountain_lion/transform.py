from datetime import datetime


def convert_document_numbers(abstract):
    for row in abstract.document_list:
        # Reception numbers prior to 1990 start with the letter "R"
        # Reception numbers between 01/01/1990 and 10/31/1995 start with the last two digits of the year
        y_start = datetime.strptime('1990-01-01', '%Y-%m-%d')
        # Reception numbers between 11/01/1995 and 12/31/1999 start with the letter "A"
        a_start = datetime.strptime('1995-11-01', '%Y-%m-%d')
        # Reception numbers between 01/01/2000 and 12/31/2009 start with the letter "B"
        b_start = datetime.strptime('2000-01-01', '%Y-%m-%d')
        # Reception numbers after 12/31/2009 "D"
        d_start = datetime.strptime('2009-12-31', '%Y-%m-%d')
        # Reception numbers after 12/31/2019 "E"
        e_start = datetime.strptime('2019-12-31', '%Y-%m-%d')
        #####################################################
        # IDENTIFY NUMBER, LENGTH, AND DATE #########
        number = row['Instrument_Number'][:-5]
        length = len(number)
        # print(row['Recording_Date'])
        # print(row['Recording_Date'] > d_start)
        # DETERMINE RECEPTION NUMBER CODE FOR NEW DOCUMENT NUMBER
        if row['Recording_Date'] < y_start:
            return 'R' + number
        elif row['Recording_Date'] >= y_start and row['Recording_Date'] < a_start:
            year = row['Instrument_Number'][-2:]
            if length < 6:
                return year + number.zfill(6)
            elif length == 6:
                return year + number
        elif row['Recording_Date'] >= a_start and row['Recording_Date'] < b_start:
            year = row['Instrument_Number'][-1:]
            code = 'A'
            if length < 7:
                return code + year + number.zfill(6)
            elif length == 7:
                return code + number
        elif row['Recording_Date'] >= b_start and row['Recording_Date'] < d_start:
            year = row['Instrument_Number'][-1:]
            code = 'B'
            if length < 7:
                return code + year + number.zfill(6)
            elif length == 7:
                return code + number
        elif row['Recording_Date'] >= d_start and row['Recording_Date'] < e_start:
            year = row['Instrument_Number'][-1:]
            code = 'D'
            if length < 7:
                return code + year + number.zfill(6)
            elif length == 7:
                return code + number
        elif row['Recording_Date'] >= e_start:
            year = row['Instrument_Number'][-1:]
            code = 'E'
            if length < 7:
                return code + year + number.zfill(6)
            elif length == 7:
                return code + number
        else:
            return 'Other'


def update_document_attributes(abstract):
    for document in abstract.document_list:
        document.county = abstract.county


def update_county_attributes(abstract):
    pass


def transform(abstract):
    convert_document_numbers(abstract)
    update_document_attributes(abstract)
    update_county_attributes(abstract)