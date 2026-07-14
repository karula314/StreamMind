# StreamMind

An AI-native streaming infrastructure platform that observes distributed streaming
systems, detects anomalies, and will investigate incidents with AI agents.

## v0.1: streaming foundation

The first milestone deliberately contains no LLM. It establishes a reproducible
local Kafka → Flink → Redis environment and a deterministic production-like data
simulator. AI investigation is added only after this streaming foundation is
observable and reliable.

## Local development environment (macOS)

This project uses Docker Compose for Kafka, Flink, Redis, and the simulator. The
Flink jobs themselves are built locally with Java 17 and Maven.

### 1. Install Docker Desktop and Docker Compose

Docker Compose v2 is bundled with Docker Desktop; do **not** install the legacy
standalone `docker-compose` package.

```bash
brew install --cask docker
open -a Docker
```

Wait until Docker Desktop reports that its engine is running, then verify both
the daemon and Compose plugin:

```bash
docker version
docker compose version
```

Allocate at least 8 GB of memory to Docker Desktop in **Settings → Resources**.

### 2. Install Java and Maven

Flink jobs use Java 17. Maven is used to resolve dependencies and build the job
JAR. Java 21 is intentionally not used because Flink documents it as experimental
support; Java 17 is the recommended version.

```bash
brew install --cask temurin@17
brew install maven
java -version
mvn -version
```

Expected results include a Java 17 runtime and Maven 3.9 or newer. If `java
-version` still reports an older JDK, restart the terminal and run:

```bash
export JAVA_HOME="$(/usr/libexec/java_home -v 17)"
export PATH="$JAVA_HOME/bin:$PATH"
```

Add those two lines to `~/.zshrc` only if Java 17 does not become the default
after a new terminal session.

### 3. Start and validate the platform

Start the core services:

```bash
docker compose up -d
docker compose ps
```

Validate Kafka, Redis, and the explicit topic bootstrap:

```bash
docker compose exec kafka kafka-topics --bootstrap-server kafka:29092 --list
docker compose exec redis redis-cli ping
```

The topic list must include `user-events`, `system-metrics`, `application-logs`,
`deployment-events`, and `alerts`; Redis must return `PONG`.

#### Verify Kafka locally

Use this sequence whenever you want to verify the local Kafka environment before
working on a Flink job. Kafka runs in KRaft mode, so no ZooKeeper process is
expected or required.

Start only Kafka and its one-time topic bootstrap container:

```bash
docker compose up -d kafka kafka-init
docker compose ps kafka kafka-init
```

Expected result:

- `kafka` has status `running (healthy)`.
- `kafka-init` has status `exited (0)`. It is intentionally a one-time container
  that creates the platform topics and then exits successfully.

List the platform topics:

```bash
docker compose exec kafka kafka-topics \
  --bootstrap-server kafka:29092 --list
```

Expected result: `alerts`, `application-logs`, `deployment-events`,
`system-metrics`, and `user-events` all appear. Kafka may also show internal
topics beginning with `__` after clients connect.

Perform an end-to-end broker check without affecting platform data. Create a
temporary topic, publish one JSON event, and consume it back:

```bash
docker compose exec kafka kafka-topics \
  --bootstrap-server kafka:29092 \
  --create --if-not-exists --topic kafka-local-check \
  --partitions 1 --replication-factor 1

printf '%s\n' '{"event_id":"local-check","event_type":"health_check"}' \
  | docker compose exec -T kafka kafka-console-producer \
      --bootstrap-server kafka:29092 --topic kafka-local-check

docker compose exec kafka kafka-console-consumer \
  --bootstrap-server kafka:29092 --topic kafka-local-check \
  --from-beginning --max-messages 1 --timeout-ms 10000
```

Expected result: the consumer prints exactly this event, then exits:

```json
{"event_id":"local-check","event_type":"health_check"}
```

Remove the temporary verification topic when finished:

```bash
docker compose exec kafka kafka-topics \
  --bootstrap-server kafka:29092 --delete --topic kafka-local-check
```

If Kafka does not become healthy, inspect its startup logs first:

```bash
docker compose logs kafka --tail=100
```

On macOS, also confirm Docker Desktop is running and has at least 8 GB allocated
under **Settings → Resources**.

Start a normal-traffic simulation:

```bash
docker compose --profile simulator up --build simulator
```

Useful endpoints:

| Service | Address |
| --- | --- |
| Flink dashboard | http://localhost:8081 |
| Kafka broker (host clients) | `localhost:9092` |
| Redis | `localhost:6379` |

### 4. Build and submit a Java Flink job

The first job has not been added yet, but the Maven project is ready. Once a job
exists, build and submit it with:

```bash
cd flink
mvn package
docker compose -f ../docker-compose.yml cp target/streammind-flink-jobs-0.1.0-SNAPSHOT.jar jobmanager:/opt/flink/usrlib/
docker compose -f ../docker-compose.yml exec jobmanager flink run /opt/flink/usrlib/streammind-flink-jobs-0.1.0-SNAPSHOT.jar
```

### 5. Stop or reset the environment

To stop the environment while retaining Redis data:

```bash
docker compose down
```

To remove all local data as well:

```bash
docker compose down -v
```

See [the Week 1 environment guide](docs/week-1-environment.md) for validation,
topics, and the initial development plan.
