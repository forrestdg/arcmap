sqlite3.exe ..\Data\Randstad\db.sqlite <..\scripts\param_randstad.sql
..\scripts\compute.py ..\Data\Randstad\db.sqlite
sqlite3.exe ..\Data\Randstad\db.sqlite <..\scripts\export_randstad.sql
pause