import arcpy
import os, sys

RELOCATE_RATE = 0.25
LAYER_NAME = "Randstad_wijk"
def main():
    ws = r"C:\Documents and Settings\Pham Thi Hong Ha\Desktop\Scenarios.gdb"
    arcpy.env.workspace = ws

    # compute the number of jobs to be relocated
    no_relocated_jobs = 0
    rows = arcpy.SearchCursor(LAYER_NAME,"Centres in ('old','old2')")
    for row in rows:
        no_relocated_jobs += int(row.no_jobs*RELOCATE_RATE)

    # count the number of communes in new center
    no_new_center_communes = 0
    rows = arcpy.SearchCursor(LAYER_NAME,
                              "Centres in ('new1', 'new2')")
    for row in rows:
        no_new_center_communes +=1
    new_job_per_commune = 1.0*no_relocated_jobs/no_new_center_communes

    # update jobs for old and new centers
    rows = arcpy.UpdateCursor(LAYER_NAME)
    count = 0
    for row in rows:
        if row.centres in ("old","old1"):
            row.jobs_scenarios = (row.no_jobs 
                                  - int(row.no_jobs*RELOCATE_RATE))
        elif row.centres in ['new1', 'new2']:
            count += 1
            row.jobs_scenarios = (row.no_jobs + 
                                  int(new_job_per_commune))
            # if it is the last commune, add the extra jobs caused by rounding too.
            if count == no_new_center_communes:
                row.jobs_scenarios += (no_relocated_jobs 
                                       - no_new_center_communes*
                                       int(new_job_per_commune))
        else:
            row.jobs_scenarios = row.no_jobs
        rows.updateRow(row) 




if __name__ == "__main__":
    sys.exit(main())
