import os
import PyPDF2
import re

from xls_parser import text_from_xls

PDFS_PATH = ('all_files_here')

files_to_process = []


def path_scan(path):
    all_files = []
    direct = os.scandir(path)
    for el in direct:
        if el.is_file():
            all_files.append(os.path.join(path, el.name))
        elif el.is_dir():
            all_files += path_scan(os.path.join(path, el.name))
    return all_files


def file_scan(list_of_files):
    for file in list_of_files:
        if file.endswith('xls'):
            if 'United Overseas Bank' in text_from_xls(file):
                if not file.startswith('UOB_XLS'):
                    files_to_process.append((file, 'UOB_XLS'))
                    continue
        if file.endswith('.csv'):
            # if re.match(r'\d{4}-\d\d-\d\d-\d\d-\d\d-\d\d'):
            with open(file) as csv_text:
                for l in csv_text:
                    if 'NTUC-OCBC' in l:
                        if not file.startswith('OCBC_CSV'):
                            files_to_process.append((file, 'OCBC_CSV'))
                            break
                    if 'POSB' in l or 'DBS' in l:
                        if not file.startswith('DBS_CSV'):
                            files_to_process.append((file, 'DBS_CSV'))
                            break
                    if 'Current Account Personal' in l:
                        if not file.startswith('CURR_CSV'):
                            files_to_process.append((file, 'CURR_CSV'))
                            break
        if file.endswith('.pdf'):
            with open(file, 'rb') as pdf:
                reader = PyPDF2.PdfFileReader(pdf)
                info = reader.getDocumentInfo()
                try:
                    if info['/Producer'] == 'StreamServe Communication Server 5.6.2 GA Build 374 (64 bit)' and \
                            info['/Author'] == 'DBS' and \
                            info['/Title'] == 'DBS DEBIT':
                        if not file.startswith('DBSD'):
                            files_to_process.append((file, 'DBSD'))
                        continue
                except KeyError:
                    pass
                try:
                    if info['/Producer'] == 'StreamServe Communication Server 5.6.2 GA Build 374 (64 bit)' and \
                            info['/Author'] == 'DBS' and \
                            info['/Subject'] == 'CreditCard Statement':
                        if not file.startswith('DBSCR'):
                            files_to_process.append((file, 'DBSCR'))
                        continue
                except KeyError:
                    pass
                try:
                    if info['/Producer'] == 'StreamServe Communication Server 5.6.2 GA Build 374 (64 bit)':
                        if not file.startswith('DBSCUR'):
                            files_to_process.append((file, 'DBSCUR'))
                        continue
                except KeyError:
                    pass
                if info['/Creator'] == 'Crystal Reports':
                    if not file.startswith('OCBC_PDF'):
                        files_to_process.append((file, 'OCBC_PDF'))
                    continue


if __name__ == '__main__':
    # for f in path_scan(PDFS_PATH):
    #     print(f)
    file_scan(path_scan(PDFS_PATH))
    print('='*100)
    for i in files_to_process:
        print(i)