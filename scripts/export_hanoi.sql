/* Dump output to csv*/
SELECT "Dumping results";
.header ON
.separator ","
.output "../Data/Hanoi/jobs.csv"
select * from communes;

.output "../Data/Hanoi/access.csv"
select * from access;
