# StreamMind Project Context

## Vision

StreamMind is a production-style Streaming AI Platform built primarily
as a portfolio project for AI Infrastructure / Data Infrastructure
roles.

Long-term goals: - Demonstrate modern streaming architecture. -
Integrate traditional data engineering with LLM/AI capabilities. -
Showcase production engineering practices.

## Career Goal

Target roles: - Senior Software Engineer - AI Infrastructure Engineer -
Data Infrastructure Engineer

Target companies include OpenAI, Anthropic, Google, xAI and similar
organizations.

## Tech Stack

Core: - Java - Apache Flink - Apache Kafka - Redis - Docker Compose -
Git / GitHub

Planned: - Python (AI services) - FastAPI - PostgreSQL - Vector
Database - LangGraph / LangChain - OpenAI-compatible LLM APIs

## Repository Structure (planned)

streammind/ docker/ flink/ simulator/ ai-service/ frontend/ docs/

## Current Progress (2026-07-14)

Completed:

-   Docker Compose environment created.
-   Kafka cluster configured.
-   Apache Flink configured.
-   Redis configured.
-   Kafka Event Simulator configured.
-   Local development environment can be started from Docker Compose.

Status:

Infrastructure foundation is complete.

Next Milestone:

Milestone 1 --- End-to-End Streaming Pipeline

Objectives: 1. Produce events with the Kafka Event Simulator. 2. Consume
events using Flink. 3. Perform simple event processing. 4. Write
processed results back to Kafka. 5. Verify the entire pipeline locally.

## Development Principles

-   Keep the project production-oriented.
-   Prefer clear architecture over unnecessary complexity.
-   Every milestone should be independently runnable.
-   Keep commits small and well documented.

## Architecture Roadmap

Phase 1 Infrastructure

Phase 2 Streaming Pipeline

Phase 3 Stateful Processing

Phase 4 AI Enrichment

Phase 5 RAG & Agent

Phase 6 Production Readiness

## Session Log

### 2026-07-14

Completed: - Docker Compose environment. - Kafka. - Flink. - Redis. -
Kafka Event Simulator.

Next: Implement the first Flink streaming job.
