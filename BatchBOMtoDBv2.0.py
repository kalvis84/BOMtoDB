"""
Uses BOMtoDB as module.
Look for all *.xls file in the directory and calls:

"BOMtoDB.insert_bom_to_db(file_list[i])"
where: file_list is a list with names of all *.xls files in given directory.

for each of them.
"""
import glob
import BOMtoDB


def batch_insert_to_db():
    file_list = glob.glob1('./', '*.xls')
    for i in range(0, file_list.__len__()):
        BOMtoDB.insert_bom_to_db('MPICOSYS_COMPONENTS.db', file_list[i])


batch_insert_to_db()
