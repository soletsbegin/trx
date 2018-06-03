import os
import re

import xlrd


PATH = os.path.join('all_files_here', '')
MONTH = {
    'jan': '01',
    'feb': '02',
    'mar': '03',
    'apr': '04',
    'may': '05',
    'jun': '06',
    'jul': '07',
    'aug': '08',
    'sep': '09',
    'oct': '10',
    'nov': '11',
    'dec': '12'
}


def clean_description(description):
    return " ".join([s for s in description.split()])


def text_from_xls(input_file):
    rb = xlrd.open_workbook(input_file, formatting_info=True)
    sheet = rb.sheet_by_index(0)
    text = ''
    for rownum in range(sheet.nrows):
        row = sheet.row_values(rownum)
        for c_el in row:
            text += str(c_el)+' '
        text += '\n'
    return text


def list_from_xls(input_file):
    rb = xlrd.open_workbook(input_file, formatting_info=True)
    sheet = rb.sheet_by_index(0)
    text = []
    for rownum in range(sheet.nrows):
        row = sheet.row_values(rownum)
        text.append(row)
    return text


def uob_parser(input_file):
    text = list_from_xls(input_file)
    data = []
    fieldnames = []
    acc_type = ''
    acc_number = ''
    bank_name = 'UOB'
    for line in text:
        if 'Account Number:' in line:
            acc_number = line[1]
        if 'Account Type:' in line:
            acc_type = line[1]
        if line[0] == 'Transaction Date':
            fieldnames = line
    transactions = []
    for line in text:
        if re.match(r'\d\d \w\w\w 20\d\d', line[0]):
            trans = dict()
            for key, val in zip(fieldnames, line):
                trans[key] = val
            transactions.append(trans)

    for t in transactions:
        date = t['Transaction Date'].split()
        date = ('{}/{}/{}'.format(date[0], MONTH[date[1].lower()], date[2]))
        # print(json.dumps(t, indent=2))
        try:
            ref1 = clean_description(t['Description'])
            amount = str(t['Transaction Amount(Local)'])
        except KeyError:
            ref1 = clean_description(t['Transaction Description'])
            amount = str(t['Withdrawal'])

        data.append({
            'Bank': bank_name,
            'Account type': acc_type,
            'Account number': acc_number,
            'Person Name': '',
            'Trans Date': date,
            'Amount': amount,
            'Debit': '',
            'Credit': '',
            'ref1': ref1,
            'ref2': '',
            'ref3': '',
        })
    return data


if __name__ == '__main__':
    for file in os.listdir(PATH):
        print(file)
        uob_parser(file)
