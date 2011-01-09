/* Constants */
DROP TABLE IF EXISTS constants;
CREATE TABLE constants(
c_key TEXT,
c_val REAL
);

/* Set alpha value here */
INSERT INTO constants VALUES("beta", 0.2);
INSERT INTO constants VALUES("Tmax", 120.0 );
INSERT INTO constants VALUES("alpha", 0.2);

