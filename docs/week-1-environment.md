# Week 1: local streaming environment

## Outcome

By the end of this week, a contributor can boot the same local environment with
one command, generate named streaming scenarios, and verify that Kafka, Flink,
and Redis are healthy. This is the foundation for the Month 1 pipeline.

## Included services

| Service | Role | Local port |
| --- | --- | --- |
| Kafka (KRaft) | Event backbone | 9092 |
| Flink JobManager | Job coordination and UI | 8081 |
| Flink TaskManager | Stream processing capacity | internal |
| Redis | Online feature / aggregation sink | 6379 |
| Simulator (optional profile) | Controlled workload source | internal |

Kafka topics are created explicitly at startup: `user-events`, `system-metrics`,
`application-logs`, `deployment-events`, and `alerts`. This makes the platform
story visible from its first commit and avoids relying on Kafka auto-topic
creation.

## Validation

After `docker compose up -d`, run:

```bash
docker compose ps
docker compose exec kafka kafka-topics --bootstrap-server kafka:29092 --list
docker compose exec redis redis-cli ping
```

Expected outcomes:

- Kafka and Redis report healthy.
- The five named Kafka topics exist.
- Redis returns `PONG`.
- The Flink dashboard is reachable at http://localhost:8081.

Then launch the simulator and inspect a few records:

```bash
docker compose --profile simulator up --build simulator
# In another terminal:
docker compose exec kafka kafka-console-consumer \
  --bootstrap-server kafka:29092 --topic user-events --from-beginning --max-messages 3
```

## Week 1 work breakdown

1. Establish and validate this Compose environment.
2. Keep event schemas documented and generated deterministically by scenario.
3. Add the first Java DataStream job: event parsing, a 1-minute event-count
   window, and a Redis sink.
4. Add a smoke test that checks topic creation and one simulator event.

The LLM, vector database, and dashboard stay out of this week. Adding them before
the streaming path is working would hide the core system behavior we need to
demonstrate. Flink is intentionally pinned to 2.2: its Kafka connector is
available as a Maven artifact, while Flink 2.3 does not yet publish one.
