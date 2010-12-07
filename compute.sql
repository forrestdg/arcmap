/* Constants */
CREATE TEMP TABLE constants(
c_key text,
c_val real
);

/* Set alpha value here */
INSERT INTO constants VALUES("alpha", -(4.0/3600.0));
INSERT INTO constants VALUES("Tmax", 7200 );


/*import table*/
DROP TABLE IF EXISTS communes;
DROP TABLE IF EXISTS access;
SELECT load_extension('./libsqlitefunctions.so');
CREATE TABLE communes(
       com_id integer,
       NAME_3 text ,
       ID_4 integer ,
       NAME_4 text ,
       Shape_Leng real ,
       Rate_pop integer,
       POP2009 integer,
       Ind_job_co integer,
       Trade_job_ integer,
       Total_job_ integer ,
       ORIG_FID integer);

.separator ","
SELECT "importing job_commne.csv";
.import job_commune.csv communes
SELECT "imported job_commne.csv";

/* delete the first line which contains labels */

DELETE FROM communes WHERE rowid = 1;

/* add a sum_weighted_jobs column
sum_weighted_jobs=sigma(jobs*exp(-0.829*access_time))*/

ALTER TABLE communes ADD COLUMN sum_weighted_jobs REAL;
ALTER TABLE communes ADD COLUMN sum_weighted_labours REAL;
ALTER TABLE communes ADD COLUMN competition_factor REAL;
ALTER TABLE communes ADD COLUMN accessibility REAL;

/*import accessibility table*/
CREATE TABLE access (
       road_id integer,
       name text,
       orig_id integer,
       dest_id integer,
       Destinat_1 integer,
       Total_Seco real
);

SELECT "importing Potential_accessibility.csv";
.import Potential_accessibility.csv access

DELETE FROM access WHERE rowid = 1;

ALTER TABLE access ADD COLUMN dest_jobs INTEGER;
ALTER TABLE access ADD COLUMN dest_labours REAL;
ALTER TABLE access ADD COLUMN time_alpha REAL;
ALTER TABLE access ADD COLUMN dest_weighted_jobs REAL;
ALTER TABLE access ADD COLUMN dest_weighted_labours REAL;
ALTER TABLE access ADD COLUMN accessibilty REAL;
ALTER TABLE access ADD COLUMN dest_competition_factor REAL;

SELECT "Updating destination jobs";
UPDATE access
    SET dest_jobs =(SELECT Total_job_
                        FROM communes WHERE com_id = dest_id );

UPDATE access
    SET dest_labours = (SELECT POP2009/2
                            FROM communes WHERE com_id = dest_id );

SELECT "Computing destinations jobs and labours";
UPDATE  access SET time_alpha = ( SELECT exp(Total_Seco*
                                     (SELECT c_val FROM constants
                                          WHERE c_key IS "alpha") )) ;
UPDATE  access SET dest_weighted_jobs = dest_jobs*time_alpha;
UPDATE  access SET dest_weighted_labours = dest_labours*time_alpha;

SELECT "Computing sum_weighted_jobs for all communes";
UPDATE communes
    SET sum_weighted_jobs = (SELECT SUM(dest_weighted_jobs)
                                 FROM access
                                 WHERE orig_id = com_id
                                 AND Total_Seco < (SELECT c_val
                                                       FROM constants
                                                       WHERE c_key IS "Tmax") );

SELECT "Computing sum_weighted_labours for all communes";

UPDATE communes
    SET sum_weighted_labours = ( SELECT SUM(dest_weighted_labours)
                                     FROM access WHERE orig_id = com_id
                                     AND Total_Seco < (SELECT c_val
                                                           FROM constants
                                                           WHERE c_key IS "Tmax") );

UPDATE communes
    SET competition_factor = sum_weighted_jobs/sum_weighted_labours;

SELECT "Updating destination competition factor";
UPDATE access
    SET dest_competition_factor = ( SELECT competition_factor
                                        FROM communes
                                        WHERE com_id = dest_id );

SELECT "Computing accessibilty for all communes";
UPDATE communes
    SET accessibility = (SELECT SUM(dest_weighted_jobs*dest_competition_factor)
                             FROM access
                             WHERE orig_id = com_id
                             AND Total_Seco < (SELECT c_val
                                                   FROM constants
                                                   WHERE c_key IS "Tmax") );


/* Dump output to csv*/
SELECT "Dumping results";
.separator ","
.output jobs.csv
select * from communes;

.output access.csv
select * from access;
