import sys, os, csv, pprint
import shutil
import sqlite3
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
    csvs = {"Hanoi":{}, "Randstad":{}}

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
        run          = row['Run']
        layername          = row['Layername']
        csvs[area][scenario] = (network_csv, job_csv)
        if area not in ["Hanoi", "Randstad"]:
            raise Exception("Unrecognized zone %s"%area)

        if scenario == "0" and update_module != "":
            raise Exception("scenario must be non-scenario by convention! No update script allowed")

        if run != "x" or access_alpha == "":
            print "Skipping %s,%s scenario %s, alpha=%s, Tmax=%s"%(area, Type, scenario, alpha, Tmax)
            continue
        
        db_file   = os.path.join(results_path, 
                                 "%s_%s_%s.sqlite"%(area, Type, scenario))
        db_file_0 = os.path.join(results_path, 
                                 "%s_%s_%s.sqlite"%(area, Type, "0"))

        # load network and job into database
        # if None of the files exists:        
        network_csv = os.path.join(data_path, area, "source", network_csv)
        job_csv = os.path.join(data_path, area, "source", job_csv)

        if not os.path.exists(network_csv):
            raise Exception("missing network_csv %s"%network_csv)
        if not os.path.exists(job_csv):
            raise Exception("missing job_csv %s"%job_csv)
        
        # if db_file not exists, then try to create it
        if not os.path.exists(db_file):
            # if db_file_0 exists and scenario 0 use the same csvs
            if ( scenario != "0" and os.path.exists(db_file_0) 
                 and csvs[area].has_key("0")
                 and csvs[area]["0"] == csvs[area][scenario]
                 ):
                shutil.copyfile(db_file_0, db_file)
            # load a fresh db
            else:
                if area == "Hanoi":
                    print "loading %s, %s"%(network_csv, job_csv)
                    import load_hanoi
                    load_hanoi.load(db_file, network_csv, job_csv)
                else:
                    import load_randstad
                    load_randstad.load(db_file, network_csv)
                # add columns and constants table
                conn = sqlite3.connect(db_file)
                conn.executescript(open("add_columns.sql").read())
                conn.commit()
            # clone db_file from db_file_0
            
            # update according to scenario if needed
            if scenario != "0" and update_module !="":
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
            cursor.execute("SELECT WK_CODE FROM communes ORDER BY com_id")
            for row in cursor:
                results[area]["WK_CODE"].append(row[0])
        if area == "Hanoi" and "ID_4" not in results[area].keys():
            results[area]["ID_4"] = []
            cursor.execute("SELECT ID_4 FROM communes ORDER BY com_id")
            for row in cursor:
                results[area]["ID_4"].append(int(row[0]))

        results[area][access_alpha] = []
        results[area][access_beta] = []            
        cursor.execute("SELECT accessibility_alpha, accessibility_beta FROM communes ORDER BY com_id")
        for row in cursor:
            results[area][access_alpha].append(int(row[0]))
            results[area][access_beta].append(int(row[1]))
        print "Finished %s,%s scenario %s, alpha=%s, Tmax=%s"%(area, Type, scenario, alpha, Tmax)
        print "Updating to %s"%layername
        import arcpy
        if area == "Hanoi":
            index_dict = {}
            for i,com_id in enumerate(results['Hanoi']['com_id']):
                id4 = results['Hanoi']['ID_4'][i]
                index_dict[id4] = i

            rows = arcpy.UpdateCursor(layername)
            for row in rows:
                id4 = row.ID_4
                idx = index_dict[id4]
                exec("row.%s = results['Hanoi']['%s'][%d]"%(access_alpha,
                                                          access_alpha,
                                                          idx
                                                          ))
                exec("row.%s = results['Hanoi']['%s'][%d]"%(access_beta,
                                                          access_beta,
                                                          idx
                                                          ))
                rows.updateRow(row)
        elif area == "Randstad":
            index_dict = {}
            for i,com_id in enumerate(results['Randstad']['com_id']):
                wkcode = results['Randstad']['WK_CODE'][i]
                index_dict[wkcode] = i

            rows = arcpy.UpdateCursor(layername)
            for row in rows:
                wkcode = row.WK_CODE
                idx = index_dict[wkcode]
                exec("row.%s = results['Randstad']['%s'][%d]"%(access_alpha,
                                                          access_alpha,
                                                          idx
                                                          ))
                exec("row.%s = results['Randstad']['%s'][%d]"%(access_beta,
                                                          access_beta,
                                                          idx
                                                          ))
                rows.updateRow(row)

        # output to csv
        for an_area in ("Hanoi", "Randstad"):
            rs = results[an_area]
            keys = sorted(rs.keys())
            if len(keys) == 0:
                continue
            csv_file = os.path.join(results_path, "%s.csv"%an_area)
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
