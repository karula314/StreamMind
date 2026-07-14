# Flink jobs

Flink jobs are written in Java 17 with the DataStream API and built with Maven.
The local cluster runs Flink 2.2 because it has a published Kafka connector.

```bash
cd flink
mvn package
docker compose -f ../docker-compose.yml cp target/streammind-flink-jobs-0.1.0-SNAPSHOT.jar jobmanager:/opt/flink/usrlib/
docker compose -f ../docker-compose.yml exec jobmanager flink run /opt/flink/usrlib/streammind-flink-jobs-0.1.0-SNAPSHOT.jar
```
