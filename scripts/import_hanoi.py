import sqlite3, sys, os, shutil

def main():
    dirname     = os.path.abspath(os.path.dirname(__file__))
    data_path   = os.path.join(dirname, "..", "Data", "Hanoi")
    data_file   = os.path.join(data_path, "db.sqlite")
    script_path = os.path.join(dirname, "import_hanoi.sql")
    bin_path    = os.path.join(dirname, "..", "bin")

    if not sys.argv[2:]:
        raise Exception("2 arguments needed")

    network_csv = sys.argv[1]
    job_csv     = sys.argv[2]

    shutil.copy(network_csv, os.path.join(data_path,"Potential_accessibility.csv"))
    shutil.copy(job_csv, os.path.join(data_path,"job_commune.csv"))

    network_csv = os.path.join(data_path, network_csv)
    job_csv     = os.path.join(data_path, network_csv)

    if os.path.exists(data_file):
        raise Exception("%s exists. Remove it manually before proceding"
                        %data_file)

    print "cd %s; sqlite3 %s <%s"%(bin_path, data_file ,script_path)
    os.system("cd %s; sqlite3 db.sqlite <%s"%(bin_path, script_path))

if __name__ == '__main__':
    main()
