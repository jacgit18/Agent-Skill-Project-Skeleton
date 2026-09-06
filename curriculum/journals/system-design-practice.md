# System Design Communication Practice Log

## Mock Interview 1: 2026-08-30

**Question:** Design a distributed event streaming platform (like Kafka/Kinesis)

**Your approach:** 
- High-level architecture: Producers publish to topics via API gateway; Broker cluster stores events in partitions; Consumers pull events and track offsets; Coordination service (Zookeeper/etcd) manages broker leadership and consumer state
- Key components: Topics with partitions for parallelism; Brokers with replication (leader/followers); Consumer groups with persistent offset tracking; Append-only log on disk for each partition
- Scaling strategy: Horizontal broker addition with partition rebalancing; 3x replication for fault tolerance; automatic leader election; consumers resume from offsets on restart
- Tradeoffs articulated: Replication adds latency but provides durability; partitioning increases throughput but adds coordination complexity; persistent vs in-memory offset storage trade speed for safety

**Feedback:** 
- **What went well:** Strong grasp of core layering and tradeoffs. Clearly articulated the tension between replication latency and durability, and between partitioning throughput and coordination complexity. Shows real engineering thinking, not just reciting architecture names.
- **Follow-up questions asked:** (1) Consumer offset scenario - if a consumer processes message #100, updates offset to #101, then crashes before finishing business logic, what problem arises and how do you solve it? (2) Coordination service dependency - if Zookeeper/etcd is unavailable for 5 minutes, can producers/consumers still operate, or does the system degrade? Would you design differently?
- **Area to improve:** Move beyond components to failure modes and guarantees. System design interviews heavily probe: "What breaks? How do you know? What do you guarantee to users?" Need to deeply explain why specific choices protect against failures (e.g., why specifically 3x replication, what does it prevent, what does it NOT prevent). What delivery guarantees does the design provide, and what's the cost?

**Takeaway:** 
Failure modes and delivery guarantees are where candidates separate from those who just memorize architecture diagrams. Next time, structure thinking around: "What breaks? What does each choice prevent? What are the guarantees?" rather than just describing components and high-level tradeoffs.

---

## Design Walkthrough 1: [Date]
**Design:** [What you were designing]
**Gaps exposed:** [What questions revealed you hadn't thought through]
**Resolved:** [How you filled in the gaps]

## Design Walkthrough 2: [Date]
[repeat above]
