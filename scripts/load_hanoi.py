import sys, os, shutil, sqlite3, csv

def load(db_file, network_csv, job_csv):
    conn = sqlite3.connect(db_file)
    conn.execute("""
CREATE TABLE communes(
       com_id integer,
       NAME_3 text ,
       ID_4 integer ,
       NAME_4 text ,
       Shape_Leng real ,
       Rate_pop integer,
       Population integer,
       Ind_job_co integer,
       Trade_job_ integer,
       total_jobs integer ,
       ORIG_FID integer,
       labour integer
)""")
    
    conn.execute("""
CREATE TABLE access (
       road_id integer,
       name text,
       orig_id integer,
       dest_id integer,
       Destinat_1 integer,
       Transit_time_min real
)""")
    
    reader = csv.reader(open(job_csv))
    for i,row in enumerate(reader):
        if i == 0:
            continue
        conn.execute("""
INSERT INTO communes VALUES (%s, "%s", %s, "%s", %s, %s, %s, %s, %s, %s, %s, %s)
"""%(row[0],row[1],row[2],row[3],row[4],row[5],row[6],
     row[7],row[8],row[9],row[10],row[11],
    )) 
        
    reader = csv.reader(open(network_csv))
    for i,row in enumerate(reader):
        if i == 0:
            continue
        conn.execute("""
INSERT INTO access VALUES (%s, "%s", %s, %s, %s, %s)
"""%(row[0],row[1],row[2],row[3],row[4],row[5]))
    conn.commit()

def main():
    if not sys.argv[3:]:
        raise Exception("2 arguments needed")
    
    db_file     = sys.argv[1]
    network_csv = sys.argv[2]
    job_csv     = sys.argv[3]
    load(db_file, network_csv, job_csv)

if __name__ == '__main__':
    main()
