move ..\Data\Hanoi\db.sqlite ..\backup\Hanoi\db.sqlite
move ..\Data\Hanoi\jobs.csv ..\backup\Hanoi\jobs.csv
move ..\Data\Hanoi\access.csv ..\backup\Hanoi\access.csv

sqlite3.exe ..\Data\Hanoi\db.sqlite <..\scripts\import_hanoi.sql
sqlite3.exe ..\Data\Hanoi\db.sqlite <..\scripts\add_columns.sql
sqlite3.exe ..\Data\Hanoi\db.sqlite <..\scripts\param_hanoi.sql

sqlite3.exe ..\Data\Hanoi\db.sqlite 'UPDATE constants SET c_val = 0.2 WHERE c_key IN ("alpha", "beta")'
sqlite3.exe ..\Data\Hanoi\db.sqlite <..\scripts\compute.sql
sqlite3.exe ..\Data\Hanoi\db.sqlite <..\scripts\export_hanoi.sql
move ..\Data\Hanoi\jobs.csv ..\Data\Hanoi\jobs_0.2.csv
move ..\Data\Hanoi\access.csv ..\Data\Hanoi\access_0.2.csv

sqlite3.exe ..\Data\Hanoi\db.sqlite 'UPDATE constants SET c_val = 0.3 WHERE c_key IN ("alpha", "beta")'
sqlite3.exe ..\Data\Hanoi\db.sqlite <..\scripts\compute.sql
sqlite3.exe ..\Data\Hanoi\db.sqlite <..\scripts\export_hanoi.sql
move ..\Data\Hanoi\jobs.csv ..\Data\Hanoi\jobs_0.3.csv
move ..\Data\Hanoi\access.csv ..\Data\Hanoi\access_0.3.csv

sqlite3.exe ..\Data\Hanoi\db.sqlite 'UPDATE constants SET c_val = 0.4 WHERE c_key IN ("alpha", "beta")'
sqlite3.exe ..\Data\Hanoi\db.sqlite <..\scripts\compute.sql
sqlite3.exe ..\Data\Hanoi\db.sqlite <..\scripts\export_hanoi.sql
move ..\Data\Hanoi\jobs.csv ..\Data\Hanoi\jobs_0.4.csv
move ..\Data\Hanoi\access.csv ..\Data\Hanoi\access_0.4.csv


sqlite3.exe ..\Data\Hanoi\db.sqlite 'UPDATE constants SET c_val = 0.5 WHERE c_key IN ("alpha", "beta")'
sqlite3.exe ..\Data\Hanoi\db.sqlite <..\scripts\compute.sql
sqlite3.exe ..\Data\Hanoi\db.sqlite <..\scripts\export_hanoi.sql
move ..\Data\Hanoi\jobs.csv ..\Data\Hanoi\jobs_0.5.csv
move ..\Data\Hanoi\access.csv ..\Data\Hanoi\access_0.5.csv


sqlite3.exe ..\Data\Hanoi\db.sqlite 'UPDATE constants SET c_val = 1.0 WHERE c_key IN ("alpha", "beta")'
sqlite3.exe ..\Data\Hanoi\db.sqlite <..\scripts\compute.sql
sqlite3.exe ..\Data\Hanoi\db.sqlite <..\scripts\export_hanoi.sql
move ..\Data\Hanoi\jobs.csv ..\Data\Hanoi\jobs_1.0.csv
move ..\Data\Hanoi\access.csv ..\Data\Hanoi\access_1.0.csv

