# datapipe

Read data from a MySQL database into Apache Kafka, perform streaming ETL with ksqlDB, then push the results to a Postgres database.

```
git clone https://github.com/berthayes/datapipe.git
```

```
cd datapipe
```

Edit the config file for your AWS environment
```
vim yak_shaving.conf
```

Create EC2 instances (12 in this case)
```
python3 create aws_instances.py -n 12
```

```sleep 30```

```
python3 create_hosts_dot_yaml.py
```


Sanity check to ensure you can reach all EC2 instances with Ansible:`
```
ansible -i hosts.yml -m ping all
```

Configure all EC2 instances to run Dockerized demo
```
ansible-playbook -i hosts.yml all.yml
```

Create DNS records for all hosts
```
python3 name_a_host.py 
```

Create target database on Postgres server
```
psql --host=datapipe1.your_route53_domain.tld --port=5432 --user=postgres --password
CREATE DATABASE user_addy;
```

Start Debezium MySQL CDC Connector
```sql
{
  "database.allowPublicKeyRetrieval": "true",
  "name": "MySqlConnect",
  "connector.class": "io.debezium.connector.mysql.MySqlConnector",
  "tasks.max": "1",
  "errors.log.enable": true,
  "errors.log.include.messages": true,
  "database.hostname": "mysql",
  "database.port": "3306",
  "database.user": "connect_user",
  "database.password": "******",
  "database.server.name": "datapipe",
  "database.history.kafka.bootstrap.servers": "broker:29092",
  "database.history.kafka.topic": "dbhistory",
  "include.schema.changes": true,
  "include.query": true
}
```
Add more records - one every 2 seconds
```
ssh -o StrictHostKeyChecking=no -i your_aws.pem ubuntu@datapipe1.yourdomain.tld "sudo chmod 755 /home/ubuntu/add_users.sh && /home/ubuntu/add_users.sh"
```

Create a stream from the incoming MySQL data:
```SQL
CREATE STREAM USER_STREAM WITH (KAFKA_TOPIC='datapipe.userdb.lusers', VALUE_FORMAT='AVRO');
```

Sanity check to make sure we can select field/values from this stream:
```SQL
SELECT
  AFTER->ID,
  AFTER->GENDER,
  AFTER->TITLE,
  AFTER->MIDDLEINITIAL,
  AFTER->SURNAME,
  AFTER->STREETADDRESS,
  AFTER->CITY,
  AFTER->STATE,
  AFTER->ZIPCODE
  FROM  USER_STREAM
  EMIT CHANGES;
```

If that worked, create a new Stream/Topic derived from the original:
```SQL
CREATE STREAM USER_ADDY WITH (
 KAFKA_TOPIC='user_address', VALUE_FORMAT='AVRO') AS
 SELECT
  AFTER->ID,
  AFTER->GENDER,
  AFTER->TITLE,
  AFTER->MIDDLEINITIAL,
  AFTER->SURNAME,
  AFTER->STREETADDRESS,
  AFTER->CITY,
  AFTER->STATE,
  AFTER->ZIPCODE
  FROM  USER_STREAM
  EMIT CHANGES;
```
Configure the JDBC Connector to push data to Postgres:
```JSON
{
  "name": "JdbcSink",
  "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
  "tasks.max": "1",
  "errors.log.enable": "true",
  "errors.log.include.messages": "true",
  "topics": [
    "user_address"
  ],
  "connection.url": "jdbc:postgresql://postgres:5432/user_addy",
  "connection.user": "postgres",
  "connection.password": "********",
  "dialect.name": "PostgreSqlDatabaseDialect",
  "auto.create": "true"
}
```

Sanity check to make sure data is flowing to Postgres:
```
psql --host=datapipe1.yourdomain.tld --port=5432 --user=postgres --password
\c user_addy;
SELECT * FROM user_address;
```


