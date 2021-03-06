/* add a sum_weighted_jobs column
sum_weighted_jobs=sigma(jobs*exp(-0.829*access_time))*/
ALTER TABLE communes ADD COLUMN sum_weighted_jobs REAL;
ALTER TABLE communes ADD COLUMN sum_weighted_labours REAL;
ALTER TABLE communes ADD COLUMN competition_factor REAL;
ALTER TABLE communes ADD COLUMN accessibility_alpha REAL;
ALTER TABLE communes ADD COLUMN accessibility_beta  REAL;

ALTER TABLE access ADD COLUMN dest_jobs INTEGER;
ALTER TABLE access ADD COLUMN dest_labours REAL;
ALTER TABLE access ADD COLUMN time_alpha REAL;
ALTER TABLE access ADD COLUMN time_beta REAL;
ALTER TABLE access ADD COLUMN dest_weighted_jobs REAL;
ALTER TABLE access ADD COLUMN dest_weighted_jobs_beta REAL;
ALTER TABLE access ADD COLUMN dest_weighted_labours REAL;
ALTER TABLE access ADD COLUMN accessibilty REAL;
ALTER TABLE access ADD COLUMN dest_competition_factor REAL;

/* Constants */
DROP TABLE IF EXISTS constants;
CREATE TABLE constants(
c_key text,
c_val real
);

/* Set alpha value here */
INSERT INTO constants VALUES("beta", 0.5);
INSERT INTO constants VALUES("Tmax", 90.0 );
INSERT INTO constants VALUES("alpha", 0.5);
