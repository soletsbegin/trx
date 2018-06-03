import csv
import os

PATH = os.path.join('all_files_here', '')
FIELDNAMES = ['Bank', 'Account type', 'Account number', 'Person Name', 'Trans Date', 'Amount',
              'Debit', 'Credit', 'ref1', 'ref2', 'ref3']

if 'transactions.csv' not in os.listdir(os.getcwd()):
    open('transactions.csv', 'w').close()


class CsvProcessor:
    def __init__(self):
        self.main_csv = 'transactions.csv'
        self._all_data = []

    def make_data(self):
        with open(self.main_csv) as csv_file:
            reader = csv.DictReader(csv_file)
            data = []
            for i in reader:
                if i not in data:
                    data.append(i)
            self._all_data = data

    def correct(self):
        data = []
        elements = []
        for i in self._all_data:
            compare = ''.join((i['Account number'], i['Account type'],
                               i['Trans Date'], i['Amount'],
                               i['Debit'], i['Credit']))
            if compare not in elements:
                elements.append(compare)
                data.append(i)
        self._all_data = data

    def data_update(self, new_data):
        for _ in new_data:
            self._all_data += new_data

    def write_data(self):
        with open('transactions.csv', 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
            writer.writeheader()
            for d in self._all_data:
                writer.writerow(d)
