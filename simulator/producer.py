"""Generate deterministic, production-shaped event streams for local development."""

import json
import os
import random
import time
import uuid
from datetime import UTC, datetime

from confluent_kafka import Producer

BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
SCENARIO = os.getenv("STREAMMIND_SCENARIO", "normal")
EVENTS_PER_SECOND = int(os.getenv("EVENTS_PER_SECOND", "10"))

EVENT_TYPES = ("play", "pause", "resume", "skip", "like", "search")
DEVICES = ("ios", "android", "web", "tv")
COUNTRIES = ("US", "CA", "GB", "DE", "JP")


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


def delivery_report(error, message) -> None:
    if error:
        print(f"delivery failed: {error}")


def user_event(rng: random.Random) -> dict[str, str]:
    return {
        "event_id": str(uuid.uuid4()),
        "event_type": rng.choice(EVENT_TYPES),
        "user_id": f"user-{rng.randint(1, 10_000):05d}",
        "song_id": f"song-{rng.randint(1, 50_000):05d}",
        "device": rng.choice(DEVICES),
        "country": rng.choice(COUNTRIES),
        "occurred_at": now_iso(),
        "scenario": SCENARIO,
    }


def system_metric(rng: random.Random) -> dict[str, float | str]:
    lag_multiplier = 100 if SCENARIO == "consumer-lag" else 1
    return {
        "metric": "kafka_consumer_lag",
        "value": round(rng.uniform(10, 50) * lag_multiplier, 2),
        "unit": "messages",
        "service": "feature-pipeline",
        "occurred_at": now_iso(),
        "scenario": SCENARIO,
    }


def main() -> None:
    if EVENTS_PER_SECOND < 1:
        raise ValueError("EVENTS_PER_SECOND must be at least 1")

    rng = random.Random(42)
    producer = Producer({"bootstrap.servers": BOOTSTRAP_SERVERS, "client.id": "streammind-simulator"})
    interval = 1 / EVENTS_PER_SECOND
    print(f"publishing {EVENTS_PER_SECOND} events/s to {BOOTSTRAP_SERVERS} (scenario={SCENARIO})")

    try:
        while True:
            event = user_event(rng)
            producer.produce("user-events", key=event["user_id"], value=json.dumps(event), on_delivery=delivery_report)
            if rng.randint(1, EVENTS_PER_SECOND) == 1:
                metric = system_metric(rng)
                producer.produce("system-metrics", key=metric["service"], value=json.dumps(metric), on_delivery=delivery_report)
            producer.poll(0)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("stopping simulator")
    finally:
        producer.flush(10)


if __name__ == "__main__":
    main()
