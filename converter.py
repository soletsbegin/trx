import os

from csv_processor import CsvProcessor
from ocbc_parser import bank_ocbc_pdf_cleaner
from dbs_parser import dbs_debit_cleaner, dbs_credit_cleaner, dbs_current_cleaner
from csv_parser import dbs_csv_parser, ocbc_csv_parser
from xls_parser import uob_parser
from file_scan import scan_path


PDFS_PATH = os.path.join('all_files_here', '')


def main():
    proc = CsvProcessor()
    proc.make_data()
    files = [f for f in os.listdir(PDFS_PATH) if f.endswith('.pdf') or not f.startswith('processed_')]
    for f in files:
        os.system('pdftotext -layout {}{}'.format(PDFS_PATH, f))
        # os.rename(PDFS_PATH + f, PDFS_PATH+'processed_%s'%f)

    text_files = [f for f in os.listdir(PDFS_PATH) if f.endswith('.txt')]

    for f in files:
        if f.endswith('.csv'):
            if f.startswith('DBS_CSV'):
                print(f)
                proc.data_update(dbs_csv_parser(f))
            if f.startswith('OCBC_CSV'):
                print(f)
                proc.data_update(ocbc_csv_parser(f))
            if f.startswith('CURR_CSV'):
                print(f)
                proc.data_update(ocbc_csv_parser(f))
        if f.endswith('xls'):
            if f.startswith('UOB_XLS'):
                print(f)
                proc.data_update(uob_parser(f))

    for f in text_files:
        print(f)
        if f.startswith('OCBC_PDF'):
            proc.data_update(bank_ocbc_pdf_cleaner(f))
        if f.startswith('DBSD'):
            proc.data_update(dbs_debit_cleaner(f))
        if f.startswith('DBSCR'):
            proc.data_update(dbs_credit_cleaner(f))
        if f.startswith('DBSCUR'):
            proc.data_update(dbs_current_cleaner(f))
    proc.correct()
    proc.write_data()
    for f in text_files:
        os.system('rm -rf {}{}'.format(PDFS_PATH, f))


if __name__ == '__main__':
    scan_path()
    main()
