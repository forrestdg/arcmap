import import_randstad
import arcpy
import sqlite3
import sys, os
import pprint
import re
SPEED_INCREASE = 2.0
HI_SPEED_LINKS = [ 
#(r"^(Amsterdam|Utrecht|Rotterdam|\'s-Gravenhage)$", 
 #                   r"^(Amsterdam|Utrecht|Rotterdam|\'s-Gravenhage)$"),
                  (r"^Amsterdam$", r".*"),
                   ]
def main():
    data_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                             "..","Data","Randstad")

    conn = sqlite3.connect(os.path.join(data_path, "db.sqlite"
                                        ))
    import_randstad.main()

    # get city_dict 
    # example: {"Amsterdam":"1, 4, 6...", "Rotterdam": "5, 9"}
    # where 1,4,6 are id of communes inside amsterdam
    #       5, 9 are id of communes inside rotterdam
    cities = {}
    cursor = conn.cursor()
    cursor.execute("SELECT com_id, city_name from communes")

    for row in cursor:
        com_id = int(row[0])
        city_name = str(row[1])
        if city_name not in cities.keys():
            cities[city_name] = ""
        if cities[city_name] == "":
            cities[city_name] = "%d"%com_id
        else:
            cities[city_name] += ", %d"%com_id
    pprint.pprint(cities)
    # get train time    
    ic_times = {}
    city_names = sorted(cities.keys())
    N = len(city_names)
    for i in range(N):
        for j in range(N):
            if j <= i:
                continue
            c1 = city_names[i]
            c2 = city_names[j]
            # only keep cities affected by hi speed trains
            affected = False
            for link in HI_SPEED_LINKS:
                if re.match(link[0], c1) and re.match(link[1], c2):
                    affected = True
                    break
            if not affected:
                continue
            cmd = """
SELECT min(transit_time_min) FROM access
   WHERE orig_id IN (%s)
       AND dest_id in (%s)
"""%(cities[c1], cities[c2])
    
            try:
                cursor.execute(cmd)
            except:
                raise Exception("""sql errors on "%s" """%cmd)
            
            min_time = float(cursor.fetchone()[0])
            ic_times[(c1,c2)] = min_time
            ic_times[(c2,c1)] = min_time
            print "%s->%s\t:%f"%(c1,c2,min_time)
    pprint.pprint(ic_times)

    # set new transit time by substracting time gained by intercity trains.
    for (c1,c2) in ic_times.keys():
        time_reduced = ic_times[(c1,c2)]*(1.0 - 1.0/SPEED_INCREASE)
        print "Reducing transit time from from %s to %s by %f mins"%(c1, c2, time_reduced)
        cmd = """
UPDATE access SET transit_time_min = transit_time_min - %f
WHERE orig_id IN (%s)
   AND dest_id in (%s)
"""%(time_reduced, cities[c1], cities[c2])
        try:
            conn.execute(cmd)
        except:
            raise Exception("""sql errors on "%s" """%cmd)

    # update transit_time_sec (not used) for the sake of completeness.
  #   cmd ="""
# UPDATE access SET transit_time_sec = transit_time_min*60.0
# """
#     try:
#         conn.execute(cmd)
#     except:
#         raise Exception("""sql errors on "%s" """%cmd)

    conn.commit()

    print "Changing job according to scenario 1 - Randstad"
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

if __name__ == "__main__":
    sys.exit(main())
