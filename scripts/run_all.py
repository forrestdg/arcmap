import sys, os, csv, pprint
import shutil
import load_hanoi
import sqlite3
#import load_randstad 
import compute
def main():
    if sys.argv[1:]:
        input_file = sys.argv[1]
    else:
        input_file = "Data_name_convention.csv"


    dirname        = os.path.abspath(os.path.dirname(__file__))
    data_path      = os.path.join(dirname, "..", "Data")
    bin_path       = os.path.join(dirname, "..", "bin")
    results_path   = os.path.join(dirname, "..", "Data", "results")

    col_map = {}
    reader = csv.DictReader(open(input_file))
    results = {"Hanoi":{}, "Randstad":{}}

    for row in reader:
        area          = row['Area']
        Type          = row['Type']
        scenario      = row['Scenario']
        network_csv   = row['Network csv']
        job_csv       = row['Job csv']
        alpha         = float(row['alpha'])
        Tmax       = float(row['Tmax'])
        update_module = row['Update script'].replace(".py","")
        access_alpha  = row['access_alpha']
        access_beta  = row['access_beta']

        if area not in ["Hanoi", "Randstad"]:
            raise Exception("Unrecognized zone %s"%area)

        if scenario == "0" and update_module != "":
            raise Exception("scenario must be non-scenario by convention! No update script allowed")

        db_file   = os.path.join(results_path, 
                                 "%s_%s_%s.sqlite"%(area, Type, scenario))
        db_file_0 = os.path.join(results_path, 
                                 "%s_%s_%s.sqlite"%(area, Type, "0"))

        # load network and job into database
        # if None of the files exists:        
        network_csv = os.path.join(data_path, area, network_csv)
        job_csv = os.path.join(data_path, area, job_csv)

        if not os.path.exists(network_csv):
            raise Exception("missing network_csv %s"%network_csv)
        if not os.path.exists(job_csv):
            raise Exception("missing job_csv %s"%job_csv)
        
        # if db_file not exists, then try to create it
        if not os.path.exists(db_file):
            # if the db_file_0 does not exists either
            if not  os.path.exists(db_file_0):
                if area == "Hanoi":
                    load_hanoi.load(db_file_0, network_csv, job_csv)
                else:
                    load_randstad.load(db_file_0, network_csv)
                # add columns and constants table
                conn = sqlite3.connect(db_file_0)
                conn.executescript(open("add_columns.sql").read())
                conn.commit()
            # clone db_file from db_file_0
            if scenario != "0":
                shutil.copyfile(db_file_0, db_file)
            
            # update according to scenario if needed
            if scenario != "0" and "update_module":
                updater = __import__(update_module)
                updater.update(db_file)
        
        # compute stuff
        # update parameters
        conn = sqlite3.connect(db_file)
        conn.execute("UPDATE constants SET c_val = %f WHERE c_key in ('alpha','beta')"
                     %alpha)
        conn.execute("UPDATE constants SET c_val = %f WHERE c_key in ('Tmax')"
                     %Tmax)
        conn.commit()
        compute.compute(db_file)
        
        # memory_result
        cursor = conn.cursor()

        if "com_id" not in results[area].keys():
            results[area]["com_id"] = []
            cursor.execute("SELECT com_id FROM communes ORDER BY com_id")
            for row in cursor:
                results[area]["com_id"].append(int(row[0]))

        if area == "Randstad" and "WK_CODE" not in results[area].keys():
            results[area]["WK_CODE"] = []
            cursor.execute("SELECT com_id FROM communes ORDER BY com_id")
            for row in cursor:
                results[area]["WK_CODE"].append(int(row[0]))


        results[area][access_alpha] = []
        results[area][access_beta] = []            
        cursor.execute("SELECT accessibility_alpha, accessibility_beta FROM communes ORDER BY com_id")
        for row in cursor:
            results[area][access_alpha].append(int(row[0]))
            results[area][access_beta].append(int(row[1]))
        print "Finished %s, scenario %s, alpha=%s, Tmax=%s"%(area, scenario, alpha, Tmax)
        # output to csv
        for area in ("Hanoi", "Randstad"):
            rs = results[area]
            keys = sorted(rs.keys())
            if len(keys) == 0:
                continue
            csv_file = os.path.join(results_path, "%s.csv"%area)
            f = open(csv_file, 'w')
            writer = csv.writer(f)
            writer.writerow(keys)
            writer = csv.DictWriter(f, keys)

            for i, com_id in enumerate(rs['com_id']):
                row = {}
                for key in keys:
                    row[key] = rs[key][i]
                writer.writerow(row)
            f.close()

if __name__ == '__main__':
    main()
