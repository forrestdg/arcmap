move ..\Data\Hanoi\db.sqlite ..\backup\Hanoi\db.sqlite
move ..\Data\Hanoi\jobs.csv ..\backup\Hanoi\jobs.csv
move ..\Data\Hanoi\access.csv ..\abackup\Hanoi\access.csv
sqlite3.exe ..\Data\Hanoi\db.sqlite <..\scripts\import_hanoi.sql
sqlite3.exe ..\Data\Hanoi\db.sqlite <..\scripts\add_columns.sql
sqlite3.exe ..\Data\Hanoi\db.sqlite <..\scripts\param_hanoi.sql
..\scripts\compute.py ..\Data\Hanoi\db.sqlite
sqlite3.exe ..\Data\Hanoi\db.sqlite <..\scripts\export_hanoi.sql
pause