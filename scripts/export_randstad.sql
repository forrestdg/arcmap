/* Dump output to csv*/
SELECT "Dumping results";
.header ON
.separator ","
.output "../Data/Randstad/jobs.csv"
select * from communes;

.output "../Data/Randstad/access.csv"
select * from access;
