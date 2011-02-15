move ..\Data\Randstad\db.sqlite ..\backup\Randstad\db.sqlite
move ..\Data\Randstad\jobs.csv ..\backup\Randstad\jobs.csv
move ..\Data\Randstad\access.csv ..\backup\Randstand\access.csv
"C:\Python25\python.exe" ..\scripts\import_randstad.py
sqlite3.exe ..\Data\Randstad\db.sqlite <..\scripts\add_columns.sql
sqlite3.exe ..\Data\Randstad\db.sqlite <..\scripts\param_randstad.sql
..\scripts\compute.py ..\Data\Randstad\db.sqlite
sqlite3.exe ..\Data\Randstad\db.sqlite <..\scripts\export_randstad.sql
pause

