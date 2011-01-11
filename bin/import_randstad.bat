move ..\Data\Randstad\db.sqlite ..\backup\Randstad\db.sqlite
move ..\Data\Randstad\jobs.csv ..\backup\Randstad\jobs.csv
move ..\Data\Randstad\access.csv ..\abackup\Randstand\access.csv
"C:\Python26\ArcGIS10.0\python.exe" ..\scripts\import_randstad.py
sqlite3.exe ..\Data\Randstad\db.sqlite <..\scripts\add_columns.sql
