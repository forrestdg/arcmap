import arcpy
import sqlite3
import sys, os

def update(db_file):
    conn = sqlite3.connect(db_file)
    data_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                             "..","Data","Randstad")



    ws = r"C:\Documents and Settings\Pham Thi Hong Ha\Desktop\Scenarios.gdb"
    arcpy.env.workspace = ws
    LAYER_NAME = "Randstad_wijk"

    rows = arcpy.SearchCursor(LAYER_NAME)
    for row in rows:
        cmd = """
UPDATE communes SET total_jobs = %d WHERE com_id = %d;
"""%(row.Jobs_scenarios, row.OBJECTID - 1 )
        try:
            conn.execute(cmd)
        except:
            raise Exception("""sql errors on "%s" """%cmd)

    conn.commit()

def main():
    update(sys.argv[1])

if __name__ == "__main__":
    sys.exit(main())

