"""
Modules insert rows form given BOM file to SQLite database.
Database name: 'MPICOSYS_COMPONENTS.db'. If not exist- will be created.
It handles old and new BOM formats.
Only *.xml is supported. Open Office file have to be converted first.
Console use: BOMtoDB <MPICOSYS_COMPONENTS.db> <mpicosys_bom.xls>.
Module use:
    import BOMtoDB
    BOMtoDB.insert_bom_to_db(bom_file_name)
"""

import sys
import sqlite3
import xlrd
import datetime

book = None
sheet = None


def create_data_table(db_file):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS BOM_data(Date TEXT, Code TEXT, Revision TEXT, BOM_name TEXT, LineNo INT, Designator TEXT,
             Value TEXT, PPT TEXT, Footprint TEXT, MPN TEXT, QTY INT, Notes TEXT)""")
    conn.commit()
    c.close()
    conn.close()


def check_bom_presence_in_db(db_file, bom_file):
    # Opening excel file to read
    global book
    book = xlrd.open_workbook(bom_file)
    # define worksheet by index. There is only one sheet in that file.
    global sheet
    sheet = book.sheet_by_index(0)

    # checking if in cell is really "Code:" present and if next is some text
    code_title = sheet.cell(3, 1).value
    code = sheet.cell(3, 2).value
    revision = sheet.cell(4, 2).value
    bom_name = code + '_' + revision

    print("Checking BOM file...")
    if code_title == "Code:" and code.__len__() >= 3:
        print("Code is present: ", code, " len: ", code.__len__(), '.')
    else:
        print("""ERROR: "Code:" cell missing.""")
        return True

    print("Looking for BOM in DB...")
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("""SELECT BOM_name from BOM_data WHERE BOM_name=?""", [bom_name])
    bom_name_cell = c.fetchone()
    conn.commit()
    c.close()
    conn.close()

    print('BOM_name cell = ', bom_name_cell)
    if bom_name_cell is not None:
        print("ERROR: BOM already present in DB.")
        return True


def bom_to_database(db_file):
    print(sheet.nrows)

    excel_date = sheet.cell(5, 4).value  # new BOM template
    if isinstance(excel_date, float) is not True:
        print('Old BOM format?')
        excel_date = sheet.cell(9, 2).value  # old BOM template

    date = datetime.datetime(*xlrd.xldate_as_tuple(excel_date, book.datemode)).strftime('%Y-%m-%d')
    code = sheet.cell(3, 2).value
    revision = sheet.cell(4, 2).value
    bom_name = code + '_' + revision

    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    for r in range(10, sheet.nrows):
        line_no = sheet.cell(r, 0).value
        designator = sheet.cell(r, 1).value
        value = sheet.cell(r, 2).value
        ppt = sheet.cell(r, 3).value
        footprint = sheet.cell(r, 4).value
        mpn = sheet.cell(r, 5).value
        qty = sheet.cell(r, 6).value
        notes = sheet.cell(r, 7).value

        values = (date, code, revision, bom_name, line_no, designator, value, ppt, footprint, mpn, qty, notes)
        print(values)

        c.execute("""INSERT INTO BOM_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", values)

    conn.commit()
    c.close()
    conn.close()


def usage_print():
    print("USE: BOMtoDB <MPICOSYS_COMPONENTS.db> <mpicosys_bom.xls>")


def insert_bom_to_db(db_file, bom_file):
    """Main function in module. Can be called form another script"""
    print('\nfile: ', bom_file)
    # create_data_table(db_file)
    if check_bom_presence_in_db(db_file, bom_file):
        return True     # ERROR
    bom_to_database(db_file)


if __name__ == '__main__':
    """Will be called in case of direct script run"""
    arg_nr = sys.argv.__len__()

    if arg_nr != 3:
        print("ERROR: There must be two arguments")
        usage_print()
        exit(sys.exit(0))

    db_name = sys.argv[1]
    split_name = db_name.split('.')
    if split_name[1].lower() != "db":
        print(split_name[1])
        print("ERROR: First argument must be database [.db] file.")
        usage_print()
        exit(sys.exit(0))

    bom_name_xls = sys.argv[2]
    split_name = bom_name_xls.split('.')

    if split_name[1].lower() != 'xls':
        print(split_name[1])
        print("ERROR: Second argument must be BOM [.xls] file.")
        usage_print()
        exit(sys.exit(0))

    insert_bom_to_db(db_name, bom_name_xls)
