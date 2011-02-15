import math
import sqlite3
import sys, os
import pprint
import re

def main():
    data_file = sys.argv[1]
    conn = sqlite3.connect(data_file)

    cursor = conn.cursor()

    # get constants
    cmd = "SELECT * from constants"
    cursor.execute(cmd)
    for row in cursor:
        if row[0] == 'alpha':
            ALPHA = float(row[1])
        elif row[0] == 'beta':
            BETA = float(row[1])
        elif row[0] == 'Tmax':
            TMAX = float(row[1])
    
    cmd = "SELECT max(com_id) FROM communes"
    cursor.execute(cmd)
    com_id_max = int(cursor.fetchone()[0])
    N = com_id_max + 1

    com_jobs             = N*[0]
    com_labours          = N*[0]
    competition_factors   = N*[0]
    accessibility_alphas = N*[0]
    accessibility_betas  = N*[0]
    sum_weighted_jobs    = N*[0]
    sum_weighted_labours  = N*[0]

    time_matrix          = []    
    time_matrix_alpha    = []
    time_matrix_beta     = []
    dest_weighted_jobs   = []
    dest_weighted_labours = []
    com_ids = []

    cmd = "SELECT com_id, total_jobs, labour FROM communes"
    cursor.execute(cmd)
    for row in cursor:
        com_id = int(row[0])
        com_jobs[com_id]    = int(row[1])
        com_labours[com_id] = int(row[2])
        com_ids.append(com_id)

    for i in range(N):
        for m in time_matrix, time_matrix_alpha, time_matrix_beta:
            line = N*[0]
            m.append(line)

    cursor.execute("SELECT orig_id, dest_id, transit_time_min from access")
    for row in cursor:
        oid = int(row[0])
        did = int(row[1])
        t = float(row[2])        
        line = time_matrix[oid]
        line[did] = t

        line_alpha = time_matrix_alpha[oid]
        line_alpha[did] = t**ALPHA

        line_beta = time_matrix_beta[oid]
        line_beta[did] = t**BETA

        

    # i: orig
    # j: dest
    for i in range(N):
        for j in range(N):
            if time_matrix_beta[i][j] > 0:
                accessibility_betas[i] += com_jobs[j]/time_matrix_beta[i][j]

            if time_matrix_alpha[i][j] > TMAX or time_matrix_alpha[i][j] == 0:
                continue
            sum_weighted_jobs[i]    += com_jobs[j]/time_matrix_alpha[i][j]
            sum_weighted_labours[j] += com_labours[j]/time_matrix_alpha[i][j]

        if sum_weighted_labours[i] > 0:
            competition_factors[i] = sum_weighted_jobs[i]/sum_weighted_labours[i]


    for i in range(N):
        for j in range(N):
            if time_matrix_alpha[i][j] > TMAX or time_matrix_alpha[i][j] == 0:
                continue
            accessibility_alphas[i] += (com_jobs[j]/time_matrix_beta[i][j]*
                                        competition_factors[j])

    # update back to jobs table
    for com_id in com_ids:
        cmd = ("UPDATE communes SET accessibility_alpha = %f WHERE com_id = %d"%(
                accessibility_alphas[com_id], com_id))
        conn.execute(cmd)

        cmd = ("UPDATE communes SET accessibility_beta = %f WHERE com_id = %d"%(
                accessibility_betas[com_id], com_id))
        conn.execute(cmd)

        cmd = ("UPDATE communes SET competition_factor = %f WHERE com_id = %d"%(
                competition_factors[com_id], com_id))
        conn.execute(cmd)
    conn.commit()

if __name__ == "__main__":
    sys.exit(main())
