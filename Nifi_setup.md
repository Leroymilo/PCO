DBCPConnectionPool : 
- database connection URL : postgresql://postgres:password@localhost:5432/RealTime
- database driver class name : cdata.jdbc.postgresql.PostgreSQLDriver

MQTT :
- broker URI : tcp://localhost:1883
- Client ID
- Topic Filter
- Max queue size : 20

JSONtoSQL :
- JDBC Connection Pool
- Statement : INSERT
- Table Name
- Quote Column Identifiers : true
- Quote Table Identifiers : true

PutSQL :
- JDBC Connection Pool
- Support Fragmented Transactions : false
- Database Session Autocommit : true