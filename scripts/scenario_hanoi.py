import arcpy
import os, sys

RELOCATE_RATE = 0.25
LAYER_NAME = "HN_commune"
def main():
    ws = r"C:\Documents and Settings\Pham Thi Hong Ha\Desktop\Scenarios.gdb"
    arcpy.env.workspace = ws

    # compute the number of jobs to be relocated
    no_relocated_jobs = 0
    rows = arcpy.SearchCursor(LAYER_NAME,"Centres = 'old'")
    for row in rows:
        no_relocated_jobs += int(row.Total_job_commune*RELOCATE_RATE)

    # count the number of communes in new center
    no_new_center_communes = 0
    rows = arcpy.SearchCursor(LAYER_NAME,
                              "Centres in ('new1', 'new2', 'new3')")
    for row in rows:
        no_new_center_communes +=1
    new_job_per_commune = 1.0*no_relocated_jobs/no_new_center_communes

    # update jobs for old and new centers
    rows = arcpy.UpdateCursor(LAYER_NAME)
    count = 0
    for row in rows:
        if row.centres == "old":
            row.jobs_scenarios = (row.Total_job_commune 
                                  - int(row.Total_job_commune*RELOCATE_RATE))
        elif row.centres in ['new1', 'new2', 'new3']:
            count += 1
            row.jobs_scenarios = (row.Total_job_commune + 
                                  int(new_job_per_commune))
            # if it is the last commune, add the extra jobs caused by rounding too.
            if count == no_new_center_communes:
                row.jobs_scenarios += (no_relocated_jobs 
                                       - no_new_center_communes*
                                       int(new_job_per_commune))
        else:
            row.jobs_scenarios = row.Total_job_commune
        rows.updateRow(row) 




if __name__ == "__main__":
    sys.exit(main())
