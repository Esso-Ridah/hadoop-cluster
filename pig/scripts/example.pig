-- Example Pig script
data = LOAD 'input.txt' USING PigStorage(',') AS (field1:chararray, field2:int);
filtered = FILTER data BY field2 > 0;
STORE filtered INTO 'output' USING PigStorage(',');
