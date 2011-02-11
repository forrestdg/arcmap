import import_randstad
import arcpy
import sqlite3
import sys, os
def main():
    data_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                             "..","Data","Randstad")

    conn = sqlite3.connect(os.path.join(data_path, "db.sqlite"
                                        ))
    import_randstad.main()
    ## same as import_randstand until here
    ws = r"C:\Documents and Settings\Pham Thi Hong Ha\Desktop\Scenarios.gdb"
    arcpy.env.workspace = ws
    LAYER_NAME = "Randstad_wijk"

    rows = arcpy.SearchCursor(LAYER_NAME)
    for row in rows:
        cmd = """
UPDATE communes SET labour = %d WHERE com_id = %d;
"""%(row.labor_scenario, row.OBJECTID - 1 )
        try:
            conn.execute(cmd)
        except:
            raise Exception("""sql errors on "%s" """%cmd)

    conn.commit()

if __name__ == "__main__":
    sys.exit(main())

