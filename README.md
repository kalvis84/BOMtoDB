# BOMtoDB
Take Bill of material in .xls and put data into a sqlite database.

			BOMtoDB.py
Module inserts rows form given BOM file to SQLite database.
Database name: 'MPICOSYS_COMPONENTS.db'. If not exist- will be created.
It handles old and new BOM formats.
Only *.xml is supported. Open Office file have to be converted first.
Console use: BOMtoDB <mpicosys bom file>.
Module use:
    import BOMtoDB
    BOMtoDB.insert_bom_to_db(bom_file_name)
***********************************************************************

			BatchBOMtoDBv1.0.py
Look for all *.xls file in the directory and calls:

"python BOMtoDB.py file_name.xls"

for each of them.
***********************************************************************

			BatchBOMtoDBv2.0.py
Uses BOMtoDB as module.
Look for all *.xls file in the directory and calls:

"BOMtoDB.insert_bom_to_db(file_list[i])"
where: file_list is a list with names of all *.xls files in given directory.

for each of them.
***********************************************************************
