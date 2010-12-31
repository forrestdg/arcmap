/* Constants */
DROP TABLE IF EXISTS constants;
CREATE TABLE constants(
c_key text,
c_val real
);

/* Set alpha value here */
INSERT INTO constants VALUES("beta", -(3.0/60.0));
INSERT INTO constants VALUES("Tmax", 120.0 );
INSERT INTO constants VALUES("alpha", 0.2);

