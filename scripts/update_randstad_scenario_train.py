import sqlite3
import sys, os
import pprint
import re
import time
SPEED_INCREASE = 2.0
HI_SPEED_STATIONS = [ "WK036300", # Amsterdam: 
                      "WK059901", # Rotterdam
                      "WK051828", # Den Haag
                      "WK034406", # Utrecht
                      ]
CONNECTION_TIME = 2 # suppose that each connection through the HISPEED line takes 2 min.

def update(db_file):
    conn = sqlite3.connect(db_file)
    data_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                             "..","Data","Randstad")

    # get city_dict 
    # example: {"Amsterdam":"1, 4, 6...", "Rotterdam": "5, 9"}
    # where 1,4,6 are id of communes inside amsterdam
    #       5, 9 are id of communes inside rotterdam

    cities = {}
    cursor = conn.cursor()

    cursor.execute("SELECT com_id, name, WK_CODE, city_name from communes")

    hi_speed_communes = []
    HS_ids = []
    communes = []
    for row in cursor:
        com_id    = int(row[0])
        name      = str(row[1])
        code      = str(row[2])
        city_name = str(row[3])
        communes.append((com_id, name, code, city_name))
        if code in HI_SPEED_STATIONS:
            hi_speed_communes.append((com_id, name, code, city_name))
            HS_ids.append(com_id)

        if city_name not in cities.keys():
            cities[city_name] = ""
        if cities[city_name] == "":
            cities[city_name] = "%d"%com_id
        else:
            cities[city_name] += ", %d"%com_id
    #pprint.pprint(cities)
    print "Communes having a hispeed station:"
    pprint.pprint(hi_speed_communes)

    # Read access table back into matrix
    # get train time    
    N = len(communes)
    time_matrix = []
    
    for i in range(N):
        line = N*[0]
        time_matrix.append(line)

    cursor.execute("SELECT orig_id, dest_id, transit_time_min from access")
    for row in cursor:
        oid = int(row[0])
        did = int(row[1])
        t = float(row[2])        
        line = time_matrix[oid]
        line[did] = t
    
    # update time for connections made by hispeed trains
    HS_links = []
    for i in HS_ids:
        for j in HS_ids:
            if i == j:
                continue
            time_matrix[i][j] /= SPEED_INCREASE
            HS_links.append((i,j,time_matrix[i][j]))
    # for all other communes, compute if a time gain could be made by
    # making ONE connection through the HISPEED network
    print "New travel time for HISPEED links:"
    pprint.pprint(HS_links)

    time_gains = [] # (oid, did, amount, connection)
    one_stops = 0
    two_stops = 0    
    for i in range(N):
        for j in range(i+1,N):
            # both communes already have their hispeed 
            # station.
            if i in HS_ids and j in HS_ids:
                continue
            old_time = time_matrix[i][j]
            time_gain = None
            for hs_orig,hs_dest, hs_time in HS_links:
                # skip if hispeed time > current travel time
                if old_time <= hs_time:
                    continue

                # skip if hispeed time + time travel to hs_origin 
                #      > current travel time
                new_time = time_matrix[i][hs_orig] + hs_time
                if old_time <= new_time:
                    continue

                # skip total_time > current travel time
                new_time = time_matrix[hs_dest][j] + new_time
                if old_time <= new_time:
                    continue

                if i == hs_orig or j == hs_dest:
                    stops = 1
                else:
                    stops = 2

                new_time += stops* CONNECTION_TIME
                # skip if total_time (connection included) > current travel time
                if time_matrix[i][j] <= new_time:
                    continue
                
                time_matrix[i][j] = new_time
                time_matrix[j][i] = new_time

                time_gain = (i,j,old_time - new_time, hs_orig, hs_dest, stops)

            if time_gain:
                time_gains.append(time_gain)
                if stops == 1:
                    one_stops +=2
                else:
                    two_stops +=2
    # print statistics:
    print "No of improved connections: %d"%(2*len(time_gains))
    print "  Of those: %d 1-stop and %d 2-stop connections"%(one_stops, two_stops)
    max_gain = max([g[2] for g in time_gains])
    max_gain_links = [ g for g in time_gains if g[2] == max_gain ]

    # min_gain = max([g[2] for g in time_gains])
    # min_gain_links = [ g in time_gains if g[2] = max_gain ]

    print "Max gain: %f min. Between:"%max_gain
    for l in max_gain_links:
        orig = [ c for c in communes if c[0] == l[0]][0]
        dest = [ c for c in communes if c[0] == l[1]][0]
        hs_orig = [ c for c in hi_speed_communes if c[0] == l[3] ][0]
        hs_dest = [ c for c in hi_speed_communes if c[0] == l[4] ][0]

        print "    %s-%s and %s-%s with HS_link: %s-%s"%(orig[3].upper(), orig[1], 
                                                         dest[3].upper(), dest[1],
                                                         hs_orig[3], hs_dest[3])

    print "Min gain: %f min"%min([g[2] for g in time_gains])
                

    print  "Updating all those number back to database"
    percentage = 0.0
    N= len(time_matrix)
    count = 0
    conn.execute("DELETE FROM access")
    conn.commit()
    for i in range(N):
        for j in range(N):
            count += 1
            new_perc = count*100.0/N/N
            if new_perc - percentage > 5:
                print "Done %f percents."%new_perc
                percentage = new_perc
            for orig_id, dest_id in ( (i,j), (j,i)):
                cmd = """
    INSERT INTO access (transit_time_min, orig_id , dest_id)
        VALUES ( %f , %d , %d)
    """%( time_matrix[orig_id][dest_id], orig_id , dest_id)
                try:
                    conn.execute(cmd)
                except:
                    raise Exception("""sql errors on "%s" """%cmd)
        conn.commit()
    return

def main():
    update(sys.argv[1])

if __name__ == "__main__":
    sys.exit(main())
