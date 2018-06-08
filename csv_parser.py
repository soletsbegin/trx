import csv
import os
import re

from google_sheet_downloader import get_sheet

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


def get_text_from_dbs_csv(input_file):
    with open(input_file) as csv_file:
        reader = csv.DictReader(csv_file)
        text = ''
        for l in reader:
            text += " ".join(l[None])+'\n'
        return text


def get_text_from_ocbc_csv(input_file):
    with open(input_file) as csv_text:
        return [line.strip() for line in csv_text]


def clean_description(description):
    return " ".join([s for s in description.split()])


def dbs_csv_parser(input_file):
    text = get_text_from_dbs_csv(input_file)
    with open(input_file) as csv_file:
        reader = csv.DictReader(csv_file)
        lines = list(l[None] for l in reader)
    data = []
    temp_data = []
    fieldnames = []

    bank_name = 'DBS'
    acc_type = re.search(r'Account Details For: ([\w ]+) +\d', text).group(1)
    acc_number = re.search(r'Account Details For: [\w ]+ +([-\d]+)', text).group(1)
    p_name = ''

    for line in lines:
        if line[0] == 'Transaction Date':
            fieldnames = line
    for line in lines:
        if re.match(r'\d\d \w{3} 20\d\d', line[0]):
            line_dict = dict()
            for field, info in zip(fieldnames, line):
                line_dict[field] = info
            temp_data.append(line_dict)

    for t in temp_data:
        date = t['Transaction Date'].split()
        date = ('{}/{}/{}'.format(date[0], MONTH[date[1].lower()], date[2]))
        local_dict_one_trans = {
            'Bank': bank_name,
            'Account type': acc_type,
            'Account number': acc_number,
            'Person Name': p_name,
            'Trans Date': date,
            'Amount': '',
            'Debit': t['Debit Amount'].strip(),
            'Credit': t['Credit Amount'].strip()
        }
        try:
            local_dict_one_trans.update({
                'ref1': clean_description(t['Transaction Ref1']),
                'ref2': clean_description(t['Transaction Ref2']),
                'ref3': clean_description(t['Transaction Ref3']),
            })
        except KeyError:
            local_dict_one_trans.update({
                'ref1': clean_description(t['Client Reference']),
                'ref2': clean_description(t['Additional Reference']),
                'ref3': clean_description(t['Reference']),
            })
        data.append(local_dict_one_trans)
    return data


def get_transactions_ocbc(list_of_lines):
    transactions = []
    for n in range(len(list_of_lines)):
        trans = []
        if re.match(r'\d\d/\d\d/\d\d\d\d,\d\d/\d\d/\d\d\d\d', list_of_lines[n]):
            trans.append(list_of_lines[n])
            next_index = n + 1
            if re.match(r'\d\d/\d\d/\d\d\d\d,\d\d/\d\d/\d\d\d\d', list_of_lines[next_index]):
                pass
            else:
                trans.append(list_of_lines[next_index])
        transactions.append(trans)
    return [tr for tr in transactions if len(tr) > 0]


def ocbc_csv_parser(input_file):
    text = get_text_from_ocbc_csv(input_file)
    transactions = get_transactions_ocbc(text)
    text = ' '.join(text)
    data = []
    bank_name = 'OCBC'
    account = re.search(r'Account details for:,([ \w-]+) ([\d-]+)', text)
    acc_type, acc_number = account.group(1), account.group(2)
    p_name = ''

    for t in transactions:
        info = re.search(r'(\d\d/\d\d/\d\d\d\d)[\d/,]+([\w ,]+)[\",]([\d,]+.\d\d)', t[0])
        date = info.group(1)
        ref1 = info.group(2)
        amount = info.group(3).replace(',', '')
        trans = {
            'Bank': bank_name,
            'Account type': acc_type.strip(),
            'Account number': acc_number.strip(),
            'Person Name': p_name,
            'Trans Date': date,
            'Amount': amount,
            'Debit': '',
            'Credit': '',
            'ref1': clean_description(ref1),
            'ref2': '',
            'ref3': ''
        }
        try:
            trans['ref2'] = t[1]
        except IndexError:
            pass
        data.append(trans)
    return data


def google_sheet_parser():
    transactions = get_sheet()
    data = []
    for t in transactions:
        date = t['Timestamp'].split()[0]
        data.append({
            'Bank': '',
            'Account type': t['Type [Row 1]'],
            'Account number': '',
            'Person Name': '',
            'Trans Date': date,
            'Amount': t['AMOUNT'],
            'Debit': '',
            'Credit': '',
            'ref1': t['DESCRIPTION'],
            'ref2': '',
            'ref3': '',
        })
    return data


if __name__ == '__main__':
    pass
