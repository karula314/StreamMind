# Simulator

The simulator emits reproducible, schema-defined streams instead of random
unrelated records. It models a music-service workload and reserves named scenarios
for controlled incident demonstrations.

Run it through Compose:

```bash
docker compose --profile simulator up --build simulator
```

Switch to a consumer-lag incident scenario:

```bash
STREAMMIND_SCENARIO=consumer-lag EVENTS_PER_SECOND=100 docker compose --profile simulator up --build simulator
```
