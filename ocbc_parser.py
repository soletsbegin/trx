import re


def clean_description(description):
    return " ".join([s for s in description.split()])


def bank_ocbc_pdf_cleaner(text_file):
    with open(text_file) as file:
        text = [l for l in file.readlines()]
    text = ''.join(text)
    data = []
    bank_name = 'OCBC'
    acc_type = re.search(r'\n(.+? Account)', text).group(1)
    acc_number = re.search(r'Account.+?([\d-]+)', text).group(1)
    transactions = re.finditer(r'(\d\d/\d\d/\d\d\d\d)[ ]+'
                               r'(\d\d/\d\d/\d\d\d\d) +'
                               r'([\w ]+) +'
                               r'([\d,.]+)\n +'
                               r'([\w.,-_ ]+)[\n ]+', text)
    transactions2 = re.finditer(r'(\d\d/\d\d/\d\d\d\d)[ ]+'
                                r'(\d\d/\d\d/\d\d\d\d) +'
                                r'([\w ]+) +'
                                r'([\d,.]+)\n\d\d/\d\d/\d\d\d\d', text)
    for t in transactions:
        if len(t.group(3)) > 40:
            debit = ''
            credit = t.group(4)
        else:
            credit = ''
            debit = t.group(4)
        data.append({
            'Bank': bank_name,
            'Account type': acc_type,
            'Account number': acc_number,
            'Person Name': '',
            'Trans Date': t.group(1).strip(),
            'ref1': clean_description(t.group(3)),
            'Amount': '',
            'Debit': debit,
            'Credit': credit,
            'ref2': clean_description(t.group(5)),
            'ref3': ''
        })
    for t in transactions2:
        if len(t.group(3)) > 40:
            debit = ''
            credit = t.group(4)
        else:
            credit = ''
            debit = t.group(4)
        data.append({
            'Bank': bank_name,
            'Account type': acc_type,
            'Account number': acc_number,
            'Person Name': '',
            'Trans Date': t.group(1),
            'ref1': clean_description(t.group(3)),
            'Debit': debit,
            'Credit': credit,
            'ref2': '',
            'ref3': '',
            'Amount': '',
        })
    return data
