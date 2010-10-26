/*import jobs table*/
SELECT load_extension('./libsqlitefunctions.so');
CREATE TABLE jobs(
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
.import job_commune.csv jobs

/* delete the first line which contains labels */
DELETE FROM jobs WHERE rowid = 1;
/* add a score column score=sigma(jobs*exp(-0.829*access_time))*/
ALTER TABLE jobs ADD COLUMN score REAL;

/*import accessibility table*/
CREATE TABLE access (
       road_id integer,
       orig_id integer,
       dest_id integer,
       OriginID integer,
       Destinatio integer,
       Destinat_1 integer,
       Total_Seco real
);

.import Potential_accessibility.csv access

DELETE FROM access WHERE rowid = 1;

ALTER TABLE access ADD COLUMN dest_jobs INTEGER;
ALTER TABLE access ADD COLUMN dest_score REAL;

UPDATE access SET dest_jobs = 
     ( SELECT Total_job_ FROM jobs WHERE com_id = dest_id );

UPDATE  access SET dest_score = (SELECT dest_jobs*exp(-1.0/3600.0*Total_Seco) ) ;

UPDATE jobs SET score = (SELECT SUM(dest_score) FROM access WHERE orig_id = com_id);

/* Dump output to csv*/

.separator ","
.output jobs.csv
select * from jobs;

.output access.csv
select * from access;
