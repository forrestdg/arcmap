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

