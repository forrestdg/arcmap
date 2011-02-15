SELECT load_extension('../bin/libsqlitefunctions.so');

SELECT "Updating destination jobs";
UPDATE access
    SET dest_jobs =(SELECT total_jobs
                        FROM communes WHERE com_id = dest_id );

UPDATE access
    SET dest_labours = (SELECT labour
                            FROM communes WHERE com_id = dest_id );

UPDATE  access SET transit_time_min = 1 WHERE transit_time_min < 1;

SELECT "Computing destinations jobs and labours (alpha)";
UPDATE  access SET time_alpha = ( SELECT power(transit_time_min,
                                     (SELECT c_val FROM constants
                                          WHERE c_key IS "alpha") )) ;
UPDATE  access SET dest_weighted_jobs = dest_jobs/time_alpha;
UPDATE  access SET dest_weighted_labours = dest_labours/time_alpha;

SELECT "Computing destinations jobs (beta)";
UPDATE  access SET time_beta = ( SELECT power(transit_time_min,
                                     (SELECT c_val FROM constants
                                          WHERE c_key IS "beta") )) ;
UPDATE  access SET dest_weighted_jobs_beta = dest_jobs/time_beta;

SELECT "Computing sum_weighted_jobs for all communes";
UPDATE communes
    SET sum_weighted_jobs = (SELECT SUM(dest_weighted_jobs)
                                 FROM access
                                 WHERE orig_id = com_id
                                 AND transit_time_min < (SELECT c_val
                                                       FROM constants
                                                       WHERE c_key IS "Tmax") );

SELECT "Computing sum_weighted_labours for all communes";

UPDATE communes
    SET sum_weighted_labours = ( SELECT SUM(dest_weighted_labours)
                                     FROM access WHERE orig_id = com_id
                                     AND transit_time_min < (SELECT c_val
                                                           FROM constants
                                                           WHERE c_key IS "Tmax") );

UPDATE communes
    SET competition_factor = sum_weighted_jobs/sum_weighted_labours;

SELECT "Updating destination competition factor";
UPDATE access
    SET dest_competition_factor = ( SELECT competition_factor
                                        FROM communes
                                        WHERE com_id = dest_id );

SELECT "Computing accessibilty_alpha for all communes";
UPDATE communes
    SET accessibility_alpha = (SELECT SUM(dest_weighted_jobs*dest_competition_factor)
                             FROM access
                             WHERE orig_id = com_id
                             AND transit_time_min < (SELECT c_val
                                                   FROM constants
                                                   WHERE c_key IS "Tmax") );
SELECT "Computing accessibilty_beta for all communes";
UPDATE communes
    SET accessibility_beta = (SELECT SUM(dest_weighted_jobs_beta)
                                  FROM access
                                  WHERE orig_id = com_id
                              );

/* Dump output to csv*/
SELECT "Dumping results";
.header ON
.separator ","
.output "../Data/Hanoi/jobs.csv"
select * from communes;

.output "../Data/Hanoi/access.csv"
select * from access;
