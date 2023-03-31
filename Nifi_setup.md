DBCPConnectionPool : 
- database connection URL : jdbc:postgresql://postgres01:5432/RealTime
- database driver class name : org.postgresql.Driver
- user : postgres
- password : password

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