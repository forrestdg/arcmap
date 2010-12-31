import arcgisscripting, os, sys
import sqlite3, csv

gp = arcgisscripting.create(9.3)

data_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                         "..","Data","Randstad")

gp.Workspace = data_path
conn = sqlite3.connect(os.path.join(data_path, "db.sqlite"
                                    ))
cur  = conn.cursor()
###############################################
#  Communes table
#
conn.execute("DROP TABLE IF EXISTS communes")
cmd = """CREATE TABLE IF NOT EXISTS communes(
       com_id INTEGER PRIMARY KEY,
       name TEXT,
       population INTEGER,
       nearest_centroid_id INTEGER,
       distance FLOAT,
       labour INTEGER,
       total_jobs INTEGER
)
"""
try:
    conn.execute(cmd)
except:
    raise Exception("""sql errors on "%s" """%cmd)
conn.commit()
communes = {}

shp_path = os.path.join(data_path, "Point_to_poly_closest.shp")
rows = gp.SearchCursor(shp_path, '','', 
                       "FID_1;FID_2,WK_NAAM;AANT_INW;labour;distance")

row = rows.next()
com_ids = []
# loop though all rows
while row:   
    cmd = """
INSERT INTO communes (com_id, name, 
                      population, nearest_centroid_id, labour, distance)
    VALUES (%d, "%s", %d, %d, %d, %f)
"""%(int(row.FID_1), row.WK_NAAM, int(row.AANT_INW), int(row.FID_2), int(row.labour), float(row.distance)) 
    try:
        conn.execute(cmd)
    except:
        raise Exception("""sql errors on "%s" """%cmd)
    com_ids.append(row.FID_1)
    communes[row.FID_1] = [int(row.FID_1), row.WK_NAAM, int(row.AANT_INW), 
                           int(row.FID_2), int(row.labour), float(row.distance),[]]
    row = rows.next()
    
conn.commit()

###############################################
#  centroids table
#
centroids = {}
conn.execute("DROP TABLE IF EXISTS centroids")
cmd = """CREATE TABLE IF NOT EXISTS centroids(
       cen_id INTEGER PRIMARY KEY,
       cen_no INTEGER,
       cen_name TEXT,
       cen_jobs INTEGER,
       parent_com_name TEXT,
       parent_com_id INTEGER
)
"""
conn.execute(cmd)
conn.commit()


shp_path = os.path.join(data_path, "Poly_to_point.shp")
rows = gp.SearchCursor(shp_path, '','', 
                       "FID_1;CENTROIDNR;NAME;WK_NAAM,FID_2;No_jobs")

row = rows.next()

# loop though all rows
while row:
    cmd = """
INSERT INTO centroids (cen_id, cen_no, cen_name, parent_com_name,
                       cen_jobs,  parent_com_id)
    VALUES (%d, %d, "%s","%s", %d, %d)
"""%(int(row.FID_1), int(row.CENTROIDNR), row.NAME, row.WK_NAAM, 
     int(row.No_jobs), int(row.FID_2))
    try:
        conn.execute(cmd)
    except:
        raise Exception("""sql errors on "%s" """%cmd)
    centroids[row.FID_1] = [int(row.FID_1), int(row.CENTROIDNR), 
                            row.NAME, row.WK_NAAM, 
                            int(row.No_jobs), int(row.FID_2)]
    communes[int(row.FID_2)][6].append(row.FID_1)
    row = rows.next()
    
conn.commit()

###############################################
#  Update communes' jobs (sum of enclosed centroids' jobs)
#

cmd = """
UPDATE communes 
    SET total_jobs = ( SELECT SUM(cen_jobs) FROM centroids 
                           WHERE parent_com_id = com_id)
"""
conn.execute(cmd)
conn.commit()

###############################################
#  Correct NULL values
#

conn.execute("""UPDATE communes SET labour = 0 WHERE labour < 0""")
conn.execute("""
UPDATE communes SET total_jobs = 0 
    WHERE total_jobs IS NULL""")
conn.commit()

###############################################
#  access table
#
conn.execute("DROP TABLE IF EXISTS access")
cmd="""CREATE TABLE IF NOT EXISTS access(
       orig_id INTEGER,
       dest_id INTEGER,
       transit_time REAL
)"""
try:
    conn.execute(cmd)
except:
    raise Exception("""sql errors on "%s" """%cmd)
conn.commit()

transit_times = {}

###############################################
#  Read csv file to array
#

csv_reader = csv.reader(open(os.path.join(data_path, "1-1-2000-1-12004.csv"
                                          )))

transit_time_matrix = []
i = 0
print "Reading big csv file."
for row in csv_reader:
    i += 1
    if i % 100 == 0:
        print("Reading line %d"%i)
    float_row = [ float(e) for e in row ]
    transit_time_matrix.append(float_row)
for i in com_ids:
    for j in com_ids:
        if j < i:
            continue
        cen_ids_i = []
        cen_ids_j = []
        if communes[i][5] > 0:
            cen_ids_i = [communes[i][3]]
        else:
            cen_ids_i = communes[i][6]

        if communes[j][5] > 0:
            cen_ids_j = [communes[j][3]]
        else:
            cen_ids_j = communes[j][6]

        t = None
        cen_nos_i = [ centroids[id][1] for id in cen_ids_i]
        cen_nos_j = [ centroids[id][1] for id in cen_ids_j]
        for c_i in cen_nos_i:
            for c_j in cen_nos_j:
                canditate_t = transit_time_matrix[c_i-1][c_j-1]
                if not t or canditate_t < t:
                    t = canditate_t
                if t == 0:
                    break
        cmd = """
INSERT INTO access (orig_id, dest_id, transit_time)
    VALUES (%d, %d, %f)
"""%(i,j,t)
        try:
            conn.execute(cmd)
        except:
            raise Exception("""sql errors on "%s" """%cmd)
        if i != j:
            cmd = """
    INSERT INTO access (orig_id, dest_id, transit_time)
        VALUES (%d, %d, %f)
    """%(j,i,t)
            try:
                conn.execute(cmd)
            except:
                raise Exception("""sql errors on "%s" """%cmd)
conn.commit()
