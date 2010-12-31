/*import table*/
DROP TABLE IF EXISTS communes;
DROP TABLE IF EXISTS access;

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
);

.separator ","
SELECT "importing job_commne.csv";
.import "../Data/Hanoi/job_commune.csv" communes

/* delete the first line which contains labels */

DELETE FROM communes WHERE rowid = 1;

/*import accessibility_alpha table*/
CREATE TABLE access (
       road_id integer,
       name text,
       orig_id integer,
       dest_id integer,
       Destinat_1 integer,
       Transit_time_min real
);

SELECT "importing Potential_accessibility.csv";
.import "../Data/Hanoi/Potential_accessibility.csv" access

DELETE FROM access WHERE rowid = 1;

