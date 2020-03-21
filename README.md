# excel-dbimporter
This script will automatically create a table uniquely named based on system date/time in the format of IMPORT_YYYYMMDDHHMMSS 
create columns based on the first row of the spreadsheet, and inserts the subsequent rows in the spreadsheet into that table.

You need to create a .dbconfig file comma-delimited to contain the DBHOST, DBUSER, DBPASSWORD and DBSCHEMA.
E.g.  "k2fqsdfadaffdaa.cbetxkdyhwsb.us-east-1.rds.amazonaws.com","admin","b3ztkms13ay2afdasfdasasdctlm","atlantisdev01"

To import an excel file:
python importexcel.py <xls path/filename>

To import csv file:
python importcsv.py <csv path/filename>

