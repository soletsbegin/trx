import os
import PyPDF2

from xls_parser import text_from_xls

PDFS_PATH = os.path.join('all_files_here', '')


def scan_path():
    for file in os.listdir(PDFS_PATH):
        print(file)
        if file.endswith('xls'):
            if 'United Overseas Bank' in text_from_xls(file):
                if not file.startswith('UOB_XLS'):
                    os.rename(PDFS_PATH + file, PDFS_PATH + 'UOB_XLS%s' % file)
                    continue
        if file.endswith('.csv'):
            with open(PDFS_PATH + file) as csv_text:
                for l in csv_text:
                    if 'NTUC-OCBC' in l:
                        if not file.startswith('OCBC_CSV'):
                            os.rename(PDFS_PATH + file, PDFS_PATH + 'OCBC_CSV%s' % file)
                            break
                    if 'POSB' in l or 'DBS' in l:
                        if not file.startswith('DBS_CSV'):
                            os.rename(PDFS_PATH + file, PDFS_PATH + 'DBS_CSV%s' % file)
                            break
                    if 'Current Account Personal' in l:
                        if not file.startswith('CURR_CSV'):
                            os.rename(PDFS_PATH + file, PDFS_PATH + 'CURR_CSV%s' % file)
                            break
        if file.endswith('.pdf'):
            with open(PDFS_PATH+file, 'rb') as pdf:
                reader = PyPDF2.PdfFileReader(pdf)
                info = reader.getDocumentInfo()
                try:
                    if info['/Producer'] == 'StreamServe Communication Server 5.6.2 GA Build 374 (64 bit)' and \
                            info['/Author'] == 'DBS' and \
                            info['/Title'] == 'DBS DEBIT':
                        if not file.startswith('DBSD'):
                            os.rename(PDFS_PATH + file, PDFS_PATH + 'DBSD%s' % file)
                        continue
                except KeyError:
                    pass
                try:
                    if info['/Producer'] == 'StreamServe Communication Server 5.6.2 GA Build 374 (64 bit)' and \
                            info['/Author'] == 'DBS' and \
                            info['/Subject'] == 'CreditCard Statement':
                        if not file.startswith('DBSCR'):
                            os.rename(PDFS_PATH + file, PDFS_PATH + 'DBSCR%s' % file)
                        continue
                except KeyError:
                    pass
                try:
                    if info['/Producer'] == 'StreamServe Communication Server 5.6.2 GA Build 374 (64 bit)':
                        if not file.startswith('DBSCUR'):
                            os.rename(PDFS_PATH + file, PDFS_PATH + 'DBSCUR%s' % file)
                        continue
                except KeyError:
                    pass
                if info['/Creator'] == 'Crystal Reports':
                    if not file.startswith('OCBC_PDF'):
                        os.rename(PDFS_PATH + file, PDFS_PATH + 'OCBC_PDF%s' % file)
                    continue
