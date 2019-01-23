# BOMtoDB
Take Bill of material in .xls and put data into a sqlite database.

## BOMtoDB.py
Module inserts rows form given BOM file to SQLite database.
Database name: 'MPICOSYS_COMPONENTS.db'. If not exist- will be created.
It handles old and new BOM formats.
Only *.xml is supported. Open Office file have to be converted first.
Console use: BOMtoDB <mpicosys bom file>.
Module use:\

		import BOMtoDB
		BOMtoDB.insert_bom_to_db(bom_file_name)
***********************************************************************

## BatchBOMtoDBv1.0.py
Looks for all *.xls file in the directory and, for each of them, calls:\

		python BOMtoDB.py file_name.xls
***********************************************************************

## BatchBOMtoDBv2.0.py
Uses BOMtoDB.py as module.
Looks for all *.xls file in the directory and store it in file_list array.
Than uses this array to insert all BOMs to DB.

		BOMtoDB.insert_bom_to_db(file_list[i])

where: file_list is a list with names of all *.xls files in given directory.
***********************************************************************
