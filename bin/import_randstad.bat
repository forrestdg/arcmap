move ..\Data\Randstad\db.sqlite ..\backup\Randstad\db.sqlite
move ..\Data\Randstad\jobs.csv ..\backup\Randstad\jobs.csv
move ..\Data\Randstad\access.csv ..\abackup\Randstand\access.csv
"C:\Python25\python.exe" ..\scripts\import_randstad.py "1-1-2000-1-12004.csv"
sqlite3.exe ..\Data\Randstad\db.sqlite <..\scripts\add_columns.sql
pause