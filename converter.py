import os

from csv_processor import CsvProcessor
from ocbc_parser import bank_ocbc_pdf_cleaner
from dbs_parser import dbs_debit_cleaner, dbs_credit_cleaner, dbs_current_cleaner
from csv_parser import dbs_csv_parser, ocbc_csv_parser
from xls_parser import uob_parser
from file_scan import file_scan, path_scan, files_to_process


PDFS_PATH = os.path.join('all_files_here', '')


def main():
    proc = CsvProcessor()
    proc.make_data()

    file_scan(path_scan(PDFS_PATH))

    # files = [f for f in files_to_process if f[0].endswith('.pdf')]
    # print(files)
    # for f in files_to_process:
    #     print(f[0])
    #     if f[0].endswith('pdf'):
    #         os.system('pdftotext -layout {}'.format(f[0]))

    # text_files = [f for f in os.listdir(PDFS_PATH) if f.endswith('.txt')]

    for f in files_to_process:
        current_file = f[0]
        type_of_file = f[1]
        if current_file.endswith('.csv'):
            if type_of_file == 'DBS_CSV':
                print(type_of_file, current_file)
                proc.data_update(dbs_csv_parser(current_file))
            if type_of_file == 'OCBC_CSV':
                print(type_of_file, current_file)
                proc.data_update(ocbc_csv_parser(current_file))
            if type_of_file == 'CURR_CSV':
                print(type_of_file, current_file)
                proc.data_update(ocbc_csv_parser(current_file))
        if current_file.endswith('xls'):
            if type_of_file == 'UOB_XLS':
                print(type_of_file, current_file)
                proc.data_update(uob_parser(current_file))
        if current_file.endswith('pdf'):
            print(current_file)
            text_file = current_file[:-3]+'txt'
            # os.system('pdftotext -layout {}'.format(current_file, text_file))
            # print(text_file)
            # if type_of_file == 'OCBC_PDF':
            #     proc.data_update(bank_ocbc_pdf_cleaner(text_file))
            # if f.startswith('DBSD'):
            #     proc.data_update(dbs_debit_cleaner(f))
            # if f.startswith('DBSCR'):
            #     proc.data_update(dbs_credit_cleaner(f))
            # if f.startswith('DBSCUR'):
            #     proc.data_update(dbs_current_cleaner(f))
            # proc.correct()
    # proc.write_data()
    # for f in text_files:
    #     os.system('rm -rf {}{}'.format(PDFS_PATH, f))


if __name__ == '__main__':
    main()

