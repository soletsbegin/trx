import re
import os

import pprint

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


def dbs_debit_cleaner(text_file):
    with open(text_file) as file:
        text = [l for l in file.readlines()]
    text = ''.join(text)
    data = []
    year = re.search(r' As at.+([\d]{4})', text).group(1)
    bank_name = 'DBS'
    acc_type = 'Passbook savings account'
    acc_number = re.search(r'ACCOUNT : ([\d-]+)', text).group(1)
    p_name = re.search(r'PG 1.+\n+ +([\w ]+)', text).group(1)
    trans1 = re.finditer(r'([\d]{2}) '                                  # day
                         r'([\w]{3}) +'                                 # month
                         r'([\?\.\*\(\)\# /:;\'\",_!%\w-]+)[\$ ]+'      # description 1
                         r'([\d.]+)[\sCR]+'                             # amount
                         r'(REF[\w :\.\d]+)', text)                     # description 2
    for t in trans1:
        date = ('{}/{}/{}'.format(t.group(1), MONTH[t.group(2).lower()], year))
        data.append({
            'Bank': bank_name,
            'Account type': acc_type.strip(),
            'Account number': acc_number.strip(),
            'Person Name': p_name,
            'Trans Date': date,
            'Amount': t.group(4),
            'Debit': '',
            'Credit': '',
            'ref1': clean_description(t.group(3)),
            'ref2': clean_description(t.group(5)),
            'ref3': '',
        })
    return data


def dbs_credit_cleaner(text_file):
    with open(text_file) as file:
        text = [l for l in file.readlines()]
    text = ''.join(text)
    data = []
    year = re.search(r'STATEMENT DATE.+\s+.+?(20\d\d)', text).group(1)
    bank_name = 'DBS'
    acc_type = 'Credit account'
    acc_number = re.search(r'CARD NO.:.+(\d{4}).+(\d{4}).+(\d{4}).+(\d{4})', text)
    acc_number = '-'.join((acc_number.group(1), acc_number.group(2), acc_number.group(3),acc_number.group(4))).strip()
    p_name = re.search(r'1 of \d\s+([\w ]+)', text).group(1)
    trans1 = re.finditer(r'(\d\d) '                                 # day
                         r'([A-Z]{3}) +'                            # month
                         r'([\?\.\*\(\)\# @&/:;\'\",_!%\w-]+) +'    # descr
                         r'(\d+[\d,.]+)', text)                     # amount
    for t in list(trans1)[1:]:          # from second element, because first isn't transaction
        date = ('{}/{}/{}'.format(t.group(1), MONTH[t.group(2).lower()], year))
        data.append({
            'Bank': bank_name,
            'Account type': acc_type.strip(),
            'Account number': acc_number.strip(),
            'Person Name': p_name,
            'Trans Date': date,
            'Amount': t.group(4),
            'Debit': '',
            'Credit': '',
            'ref1': clean_description(t.group(3)),
            'ref2': '',
            'ref3': '',
        })
    return data


def dbs_current_cleaner(text_file):
    with open(text_file) as file:
        text = [l for l in file.readlines()]
    text = ''.join(text)
    data = []
    year = re.search(r'As at.+(20\d\d)', text).group(1)
    bank_name = 'DBS'
    acc_type = 'POSB current account'
    acc_number = re.search(r'Account No. ([\d-]+)', text).group(1)
    p_name = re.search(r'CONSOLIDATED STATEMENT\s+([\w ]+)', text).group(1)
    transactions = get_tranc_from_current_acc(text_file)

    for t in list(transactions):
        date = ('{}/{}/{}'.format(t[0], MONTH[t[1].lower()], year))
        temp_data = {
            'Bank': bank_name,
            'Account type': acc_type.strip(),
            'Account number': acc_number.strip(),
            'Person Name': p_name,
            'Trans Date': date,
            'Amount': t[3],
            'Debit': '',
            'Credit': '',
            'ref1': t[2],
            'ref2': t[4],
            'ref3': '',
        }
        try:
            temp_data['ref3'] = t[5]
        except IndexError:
            pass
        data.append(temp_data)
    return data


def get_tranc_from_current_acc(text_file):
    with open(text_file) as file:
        lines = [l.strip() for l in file.readlines()]
    data = []
    transactions = []
    for n in range(len(lines)):
        trans = []
        if re.match(r'[0-3]\d \w\w\w ', lines[n]):
            trans.append(lines[n])
            next_index = n+1
            if re.match(r'[0-3]\d \w\w\w ', lines[next_index]):
                pass
            else:
                trans.append(lines[next_index])
                next_index += 1
                if re.match(r'[0-3]\d \w\w\w ', lines[next_index]):
                    pass
                else:
                    trans.append(lines[next_index])
        transactions.append(trans)
    transactions = [t for t in transactions if len(t) > 0]
    for t in transactions:
        processed_info = []
        unproc_info = t[0].split()
        processed_info += unproc_info[:2]
        ref1 = []
        for i in unproc_info[2:]:
            if re.match(r'\d+.\d\d', i):
                processed_info.append(' '.join(ref1))
                processed_info.append(i)
                break
            else:
                ref1.append(i)
        for element in t[1:]:
            if len(element) < 90:
                processed_info.append(element)
        data.append(processed_info)
    return [t for t in data if len(t[2]) > 0]
