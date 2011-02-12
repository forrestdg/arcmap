import import_randstad
import arcpy
import sqlite3
import sys, os
import pprint

SPEED_INCREASE = 2.0

def main():
    data_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                             "..","Data","Randstad")

    conn = sqlite3.connect(os.path.join(data_path, "db.sqlite"
                                        ))
    import_randstad.main()

    # get city_dict 
    # example: {"Amsterdam":"1 4 6...", "Rotterdam": "5 9"}
    # where 1,4,6 are id of communes inside amsterdam
    #       5, 9 are id of communes inside rotterdam
    cities = {}
    cursor = conn.cursor()
    cursor.execute("SELECT com_id, city_name from commune")
    for row in cursor:
        com_id = int(curosr[0])
        city_name = str(cursor[1])
        if name not in cities.keys():
            cities[city_name] = ""
        cities[city_name] += "%d "%com_id
    pprint.pprint(cities)

    # get train time
    ic_time = dict{}
    for c1 in cities.keys():
        for c2 in cities.keys():
            if c1 == c2:
                continue
            cmd = """
SELECT min(transit_time_min) FROM access
   WHERE orig_id IN (%s)
       AND dest_id in (%s)
"""%(cities[c1], cities[2])
    
            try:
                cursor.execute(cmd)
            except:
                raise Exception("""sql errors on "%s" """%cmd)
            
            min_time = float(cursor.fetchone()[0])
            ic_time[(c1,c2)] = min_time
    
    pprint.pprint(ic_time)

    # set new transit time by substracting time gained by intercity trains.
    for c1 in cities.keys():
        for c2 in cities.keys():
            if c1 == c2:
                continue
            time_reduced = ic_time[(c1,c2)]*(1.0 - 1.0/SPEED_INCREASE)
            
            cmd = """
UPDATE access SET transit_time_min = transit_time_min - %f
   WHERE orig_id IN (%s)
       AND dest_id in (%s)
"""%(time_reduced, cities[c1], cities[2])
            try:
                conn.execute(cmd)
            except:
                raise Exception("""sql errors on "%s" """%cmd)

    # update transit_time_sec (not used) for the sake of completeness.
    cmd ="""
UPDATE access SET transit_time_sec = transit_time_min*60.0
"""
    try:
        conn.execute(cmd)
    except:
        raise Exception("""sql errors on "%s" """%cmd)

    conn.commit()

if __name__ == "__main__":
    sys.exit(main())
