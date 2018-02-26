"""
Look for all *.xls file in the directory and calls:

"python BOMtoDB.py file_name.xls"

for each of them.
"""
import glob
import os


def batch_insert_to_db():
    file_list = glob.glob1('./', '*.xls')
    for i in range(0, file_list.__len__()):
        command = "python BOMtoDB.py " + ' ' + "MPICOSYS_COMPONENTS.db" + ' ' + file_list[i]
        os.system(command)


batch_insert_to_db()
