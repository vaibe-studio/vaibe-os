---
name: software-architecture-patterns
description: Clean Architecture, DDD, microservices, event-driven architecture, API design. Reference material (non-actionable knowledge).
license: MIT
---

# Software Architecture Patterns — Decision Reference

Practical reference for architectural styles, decomposition strategies, and API design patterns. Enables the agent and user to make informed architecture decisions based on context: team size, complexity, scalability needs, and organizational structure.

## When to use

- Starting a new project and choosing architecture style
- Evaluating whether to decompose a monolith
- Selecting API communication patterns
- Reviewing architecture decisions or conducting architecture reviews
- Planning infrastructure and deployment strategies (see `.vaibe/skills/devops-practices/SKILL.md`)
- Making build-vs-buy decisions (see `.vaibe/skills/strategy-frameworks/SKILL.md` — Wardley Maps)

---

## Layered architectures: Clean, Hexagonal, Onion

Three related patterns that share the same fundamental goal: **decouple core business logic from external concerns** (databases, APIs, UIs, frameworks). The domain is at the center; infrastructure is at the edges.

### Common principle: Dependency Rule

Dependencies point **inward**. Inner layers know nothing about outer layers. Outer layers depend on interfaces defined by inner layers, not the reverse. This makes the core testable, portable, and framework-independent.

### Hexagonal Architecture (Ports and Adapters)

Alistair Cockburn, 2005.

```
           [Adapter: REST API]
                  |
           [Port: IncomingUseCase]
                  |
          ┌───────────────────┐
          │   Application     │
          │   Core (Domain)   │
          └───────────────────┘
                  |
           [Port: OutgoingRepo]
                  |
           [Adapter: PostgreSQL]
```

- **Ports** — interfaces that define how the application interacts with the outside world (incoming: what the app offers; outgoing: what the app needs)
- **Adapters** — implementations that connect ports to specific technologies (REST controller, database driver, message queue client)
- Strength: external dependencies are fully swappable; excellent for systems with multiple frontends or integrations

### Clean Architecture

Robert C. Martin, 2012.

Four concentric layers:
1. **Entities** — enterprise-wide business rules and domain objects
2. **Use Cases** — application-specific business rules (orchestrate entities)
3. **Interface Adapters** — convert data between use cases and external formats (controllers, presenters, gateways)
4. **Frameworks and Drivers** — outermost layer (web framework, database, UI, external services)

Key addition: "Screaming Architecture" — the folder structure should scream the domain, not the framework. A project should look like "healthcare system" not "Spring Boot app."

### Onion Architecture

Jeffrey Palermo, 2008.

Concentric layers: Domain Model → Domain Services → Application Services → Infrastructure. Strongly protects the domain model from any infrastructure leakage. Best for domain-heavy systems where the model is the primary asset.

### When to use which

| Situation | Recommended |
|---|---|
| Small project, rapid prototyping | Traditional layered (simple 3-tier) |
| Complex business rules, need testability | Clean Architecture |
| Domain is the primary asset, long-lived system | Onion Architecture |
| Multiple frontends/integrations, swappable backends | Hexagonal |
| Any of the above + DDD | Hexagonal or Onion (natural fit) |

---

## Domain-Driven Design (DDD)

### Strategic patterns

| Pattern | Purpose |
|---|---|
| **Bounded Context** | Explicit boundary within which a domain model is defined and applicable. Different contexts may have different models for the same real-world concept |
| **Ubiquitous Language** | Shared vocabulary between developers and domain experts within a bounded context |
| **Context Map** | Visualization of relationships between bounded contexts (upstream/downstream, shared kernel, anti-corruption layer) |
| **Anti-Corruption Layer** | Translation layer that prevents one context's model from leaking into another |

### Tactical patterns

| Pattern | Description | Key rules |
|---|---|---|
| **Entity** | Object with unique identity that persists over time | Identity is intrinsic; encapsulates behavior, not just data |
| **Value Object** | Object defined by attributes, no identity | Immutable; equality by value; rich in domain logic; self-validating |
| **Aggregate** | Cluster of entities and value objects with a consistency boundary | One root entity; external references only to root; transactional consistency within aggregate |
| **Repository** | Abstraction for aggregate persistence | One repository per aggregate root; interface in domain, implementation in infrastructure |
| **Domain Service** | Stateless operation that doesn't naturally belong to any entity | Use when logic spans multiple aggregates or entities |
| **Domain Event** | Record of something significant that happened in the domain | Immutable; named in past tense (OrderPlaced, PaymentReceived); enables loose coupling |
| **Factory** | Encapsulates complex creation logic for aggregates or entities | Use when construction is non-trivial |

### Aggregate design heuristics

- Keep aggregates small — prefer single-entity aggregates; add entities only when true invariant requires it
- Reference other aggregates by ID, not by object reference
- Use eventual consistency between aggregates (domain events)
- One aggregate = one transaction boundary
- Microservice boundary: no smaller than an aggregate, no larger than a bounded context

---

## Monolith vs microservices

### Monolith

Single deployable unit. All modules share process, database, and deployment lifecycle.

**Advantages:** Simple deployment, debugging, testing. No network latency between modules. Single transaction boundary. Low operational overhead.

**Disadvantages:** Scaling is all-or-nothing. Large codebase can become tangled. Deployment requires full system redeploy. Technology choices affect entire system.

### Modular monolith

Single deployable unit with **strong internal module boundaries**. Modules have explicit interfaces, separate data access patterns, and enforce encapsulation.

**Advantages:** Simplicity of monolith + maintainability of good boundaries. Single deployment pipeline. No distributed systems complexity. Debugging with single stack traces. Can evolve into microservices later if needed.

**Key challenge:** Maintaining module boundaries requires discipline. Organizational pressure and convenience encourage shortcuts that erode boundaries over time.

### Microservices

Multiple independently deployable services, each owning its data and business capability.

**Advantages:** Independent deployment and scaling. Technology diversity per service. Team autonomy (Conway's Law alignment). Fault isolation.

**Disadvantages:** Distributed systems complexity (network failures, latency, eventual consistency). Operational overhead (monitoring, tracing, deployment orchestration). Data consistency challenges. Debugging across service boundaries.

### Decision framework

| Factor | Monolith / Modular monolith | Microservices |
|---|---|---|
| Team size | < 8–10 engineers | Multiple autonomous teams |
| Deployment independence needed | No | Yes — different services need different release cadences |
| Scaling requirements | Uniform or predictable | Components have very different scaling profiles |
| Domain understanding | Still discovering boundaries | Bounded contexts are well understood |
| Organizational structure | Single team or tightly coupled teams | Independent product teams (Conway's Law) |
| Operational maturity | Limited DevOps capability | Strong CI/CD, observability, container orchestration |

**Sam Newman's rule of thumb:** Start with a monolith. Extract services only when you have clear reasons and the operational capability to support them. Premature decomposition is more costly than premature monolith.

---

## Event-driven architecture (EDA)

### Core concept

Components communicate through **events** (immutable facts about things that happened) rather than direct synchronous calls. Enables loose coupling, independent scaling, and parallel processing.

### Event types

| Type | Purpose | Example |
|---|---|---|
| **Domain event** | Something significant happened in business terms | OrderPlaced, PaymentReceived |
| **Integration event** | Cross-service communication | InventoryReserved, ShipmentDispatched |
| **Notification event** | Thin event signaling something happened; consumer fetches details | OrderUpdated (ID only) |
| **Event-carried state transfer** | Event carries enough data for consumer to operate without callback | OrderPlaced { orderId, items, total, customer } |

### Event structure best practices

Events should include: event type, timestamp, correlation ID (for tracing), causation ID (what triggered this event), version (for schema evolution), payload. Events are immutable — never modify published events; publish new corrective events instead.

### CQRS (Command Query Responsibility Segregation)

Separate write model (commands that change state) from read model (queries that return data).

| Side | Responsibility | Optimization |
|---|---|---|
| **Command (write)** | Validate, enforce invariants, persist | Normalized, consistency-focused |
| **Query (read)** | Return data to clients | Denormalized, performance-focused, eventually consistent |

Write side publishes events; read side consumes events and builds optimized projections. Enables independent scaling: writes are typically 10–20% of operations, reads are 80–90%.

**When to use CQRS:** Read and write patterns are significantly different. High read-to-write ratio. Complex queries that benefit from denormalized views. Need to scale reads and writes independently.

**When NOT to use:** Simple CRUD. Low traffic. Team unfamiliar with eventual consistency. Single bounded context with straightforward queries.

### Saga pattern

Coordinates multi-step business processes across services using local transactions and compensating actions (instead of distributed transactions).

| Approach | Mechanism | Pros | Cons |
|---|---|---|---|
| **Choreography** | Services listen to events and react independently | Decoupled; simple for few steps | Hard to track overall progress; implicit flow |
| **Orchestration** | Central orchestrator coordinates steps | Explicit flow; easier monitoring | Orchestrator can become a bottleneck; coupling risk |

**Compensating actions:** If step 3 fails, execute compensations for steps 1 and 2 to undo their effects. Not all actions are perfectly reversible — design for eventual consistency and human intervention for edge cases.

---

## API design patterns

### REST

Resource-oriented architecture over HTTP. Uses standard methods (GET, POST, PUT, PATCH, DELETE) and status codes.

**Best for:** Public APIs, partner integrations, broad compatibility. Leverages HTTP caching, CDN distribution. Mature tooling (OpenAPI/Swagger). Stateless and scalable.

**Key practices:** Use nouns for resources, verbs for HTTP methods. Version APIs (URL or header). HATEOAS for discoverability (optional). Consistent error format. Pagination for collections.

### GraphQL

Query language that lets clients request exactly the data they need from a single endpoint.

**Best for:** Multiple client types needing different data shapes (web, mobile, TV). Deeply nested data that would require many REST endpoints. Rapid frontend iteration without backend changes.

**Key practices:** Schema-first design. Avoid N+1 query problems (use DataLoader). Implement query complexity limits. Persisted queries for performance. Authentication at resolver level, not just endpoint.

**Trade-offs:** Complex caching. Potential for expensive queries. Steeper learning curve. All requests are POST — standard HTTP caching doesn't work.

### gRPC

High-performance RPC framework using Protocol Buffers (protobuf) over HTTP/2.

**Best for:** Internal microservice communication where latency matters. Bidirectional streaming (real-time, IoT, telemetry). Strongly-typed contracts with code generation. Polyglot environments (generated clients for any language).

**Trade-offs:** Not browser-native (needs gRPC-Web or gateway). Binary format is not human-readable. Limited caching. Requires protobuf schema management.

### Mixed protocol strategy

| Layer | Protocol | Rationale |
|---|---|---|
| Public / Partner | REST | Compatibility, caching, discoverability |
| Client composition | GraphQL | Flexible data fetching, reduced round trips |
| Service-to-service | gRPC | Performance, type safety, streaming |

---

## Decision heuristics

- **New project, small team** → modular monolith with Clean/Hexagonal architecture; extract services later if needed
- **Complex domain with experts available** → DDD with bounded contexts; Hexagonal or Onion architecture
- **High read-to-write ratio, complex queries** → consider CQRS for the read-heavy bounded context
- **Multi-service, cross-service transactions** → Saga pattern (choreography for simple flows, orchestration for complex)
- **Multiple frontend clients with different data needs** → GraphQL composition layer over REST/gRPC backends
- **Performance-critical internal communication** → gRPC
- **Team lacks distributed systems experience** → do not start with microservices. Build a well-structured monolith first
- **"We need microservices for scalability"** → challenge assumption. Modular monolith + horizontal scaling handles most load profiles

## Anti-patterns

- **Distributed monolith** — microservices that must be deployed together, share databases, or make synchronous chains of calls; worst of both worlds
- **Anemic domain model** — entities as data containers with all logic in services; defeats DDD's purpose
- **Big Ball of Mud** — monolith without internal boundaries; all code depends on everything else
- **Premature microservices** — decomposing before understanding domain boundaries; creates the wrong services
- **CQRS everywhere** — applying CQRS to simple CRUD contexts; unnecessary complexity
- **Event soup** — publishing events for everything without clear domain semantics; consumers can't make sense of the stream
- **Shared database across services** — destroys service autonomy; creates hidden coupling
- **Framework-driven architecture** — organizing code by framework conventions instead of business domains
- **API versioning avoidance** — making breaking changes to APIs without versioning; breaks consumers

## Sources

- Martin, R.C. *Clean Architecture.* Prentice Hall, 2017. ISBN 978-0-13-449416-6
- Evans, E. *Domain-Driven Design: Tackling Complexity in the Heart of Software.* Addison-Wesley, 2003. ISBN 978-0-321-12521-7
- Newman, S. *Building Microservices (2nd ed).* O'Reilly, 2021. ISBN 978-1-492-03402-5
- Newman, S. *Monolith to Microservices.* O'Reilly, 2019. ISBN 978-1-492-07554-7
- Khononov, V. *Learning Domain-Driven Design.* O'Reilly, 2021. ISBN 978-1-098-10013-1
- Fowler, M. *Patterns of Enterprise Application Architecture.* Addison-Wesley, 2002. ISBN 978-0-321-12742-6
- Cockburn, A. *Hexagonal Architecture.* 2005. `https://alistair.cockburn.us/hexagonal-architecture/`
- Microsoft. *Tactical DDD for Microservices.* `https://learn.microsoft.com/en-us/azure/architecture/microservices/model/tactical-ddd`
- OpenGitOps. `https://opengitops.dev/` (see also `.vaibe/skills/devops-practices/SKILL.md`)
- Cross-reference: `.vaibe/skills/tech-stack-reference/SKILL.md` — project tech stack
- Cross-reference: `.vaibe/skills/devops-practices/SKILL.md` — CI/CD, deployment strategies, container orchestration
- Cross-reference: `.vaibe/skills/strategy-frameworks/SKILL.md` — Wardley Maps for build/buy/outsource decisions
