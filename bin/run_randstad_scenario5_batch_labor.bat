move ..\Data\Randstad\db.sqlite ..\backup\Randstad\db.sqlite
move ..\Data\Randstad\jobs.csv ..\backup\Randstad\jobs.csv
move ..\Data\Randstad\access.csv ..\backup\Randstad\access.csv
move ..\Data\Randstad\results\*.csv ..\backup\Randstad\
@echo off
SetLocal

set FILES=1-4-2-1-23-5.csv 1-1-2024-1-3-2004.csv
set ALPHAS=0.4
set TMAXES=90
FOR %%f in (%FILES%) do (
    "C:\Python26\ArcGIS10.0\python.exe" ..\scripts\import_randstad_scenario5_labor.py %%f
    sqlite3.exe ..\Data\Randstad\db.sqlite <..\scripts\add_columns.sql
    sqlite3.exe ..\Data\Randstad\db.sqlite <..\scripts\param_randstad.sql
    FOR %%a in (%ALPHAS%) DO (
        FOR %%t in (%TMAXES%) DO (
            sqlite3.exe  ..\Data\Randstad\db.sqlite "UPDATE constants SET c_val = %%a WHERE c_key IN ('alpha', 'beta')"		
            sqlite3.exe  ..\Data\Randstad\db.sqlite "UPDATE constants SET c_val = %%t WHERE c_key IS 'Tmax'"		
	    sqlite3.exe ..\Data\Randstad\db.sqlite "SELECT * FROM constants"
	    sqlite3.exe ..\Data\Randstad\db.sqlite <..\scripts\compute.sql
	    sqlite3.exe ..\Data\Randstad\db.sqlite <..\scripts\export_randstad.sql
	    move ..\Data\Randstad\jobs.csv ..\data\Randstad\results\jobs_scenario4__%%t_%%a_%%f
        move ..\Data\Randstad\access.csv ..\data\Randstad\results\access_scenario4__%%t_%%a_%%f
	)
    )
    move ..\Data\Randstad\db.sqlite ..\backup\Randstad\db__%%f.sqlite
)
