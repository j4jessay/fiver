# Kafka Architecture Overview

## Introduction

Now that you know **what** Kafka is, let's understand **how** it works internally. This knowledge will help you build and troubleshoot Kafka applications.

**Reading Time**: 7-10 minutes

---

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    Kafka Cluster                             │
│                                                              │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │  Broker 1  │  │  Broker 2  │  │  Broker 3  │            │
│  │            │  │            │  │            │            │
│  │ Topic A:P0 │  │ Topic A:P1 │  │ Topic A:P2 │            │
│  │ Topic B:P1 │  │ Topic B:P0 │  │ Topic C:P0 │            │
│  └────────────┘  └────────────┘  └────────────┘            │
│                                                              │
│  Coordinated by                                             │
│  ┌────────────┐                                             │
│  │ ZooKeeper  │  (or KRaft in Kafka 3.3+)                  │
│  └────────────┘                                             │
└──────────────────────────────────────────────────────────────┘
        ↑                                      ↓
  ┌────────────┐                        ┌────────────┐
  │ Producers  │                        │ Consumers  │
  │            │                        │            │
  │ - App 1    │                        │ - App A    │
  │ - App 2    │                        │ - App B    │
  │ - App 3    │                        │ - App C    │
  └────────────┘                        └────────────┘
```

### Components

1. **Producers**: Applications that send data TO Kafka
2. **Brokers**: Kafka servers that store and serve data
3. **Topics**: Logical channels for organizing data
4. **Partitions**: Subdivisions of topics for parallelism
5. **Consumers**: Applications that read data FROM Kafka
6. **ZooKeeper**: Coordination service (being replaced by KRaft)

---

## Brokers: The Kafka Servers

### What is a Broker?

A **broker** is a single Kafka server instance.

**Think of it like**:
- One physical or virtual machine running Kafka
- Each broker is identified by a unique ID (e.g., broker 0, broker 1, broker 2)

### Kafka Cluster

Multiple brokers working together form a **cluster**:

```
Production Setup:
┌─────────────────────────────────────────┐
│          Kafka Cluster                  │
│                                         │
│  Broker 1    Broker 2    Broker 3       │
│  (ID: 0)     (ID: 1)     (ID: 2)        │
│                                         │
│  Each stores different partitions       │
│  Data is replicated across brokers      │
└─────────────────────────────────────────┘
```

**Why Multiple Brokers?**
- **Scalability**: Distribute load across machines
- **Fault Tolerance**: If one fails, others take over
- **High Availability**: No single point of failure

### Our Lab Setup (Development)

In Module 1's lab, we'll start with **1 broker**:

```
Development Setup:
┌─────────────────┐
│  Single Broker  │
│   (Broker 0)    │
│                 │
│  All partitions │
│  on one server  │
└─────────────────┘
```

**Why start simple?**
- Easier to understand
- Faster setup
- Sufficient for learning
- We'll add more brokers later if needed

---

## Topics and Partitions

### Topics: Organizing Events

A **topic** is a logical category for events.

**Example Topics**:
- `user.clicks` - All user click events
- `orders` - All order events
- `vehicle.telemetry` - All vehicle sensor data (our project!)

**Naming Conventions**:
```
Good: vehicle.telemetry, user.clicks, payment.completed
Bad: data, topic1, myTopic
```

Use descriptive names with namespaces (dot notation).

### Partitions: Scaling Topics

Each topic is divided into **partitions** for parallelism:

```
Topic: vehicle.telemetry (3 partitions)

Partition 0: [msg0, msg3, msg6, msg9, ...]
Partition 1: [msg1, msg4, msg7, msg10, ...]
Partition 2: [msg2, msg5, msg8, msg11, ...]

Messages are distributed across partitions
Each partition is an ordered, immutable sequence of messages
```

### Why Partitions Matter

**1. Parallelism**
```
Single Partition:
Producer → [================] → Consumer
            1 GB/sec max

Three Partitions:
Producer → [=====] → Consumer 1  ┐
       ├→ [=====] → Consumer 2  ├→ 3 GB/sec total
       └→ [=====] → Consumer 3  ┘
```

**2. Ordering Guarantees**
- ✅ **Within a partition**: Messages are strictly ordered
- ❌ **Across partitions**: No ordering guarantee

**3. Distribution Across Brokers**
```
Broker 1: Partition 0, Partition 3
Broker 2: Partition 1, Partition 4
Broker 3: Partition 2, Partition 5
```

### How Messages Are Assigned to Partitions

**Option 1: No Key (Round-Robin)**
```python
producer.send("vehicle.telemetry", value="sensor data")
# Kafka distributes evenly: P0, P1, P2, P0, P1, P2, ...
```

**Option 2: With Key (Hash-Based)**
```python
producer.send("vehicle.telemetry", key="vehicle_123", value="data")
# Same key always goes to same partition
# vehicle_123 → always Partition 1
```

**Why use keys?**
- Maintain order for related events (e.g., all events for one user)
- Enable stateful processing

---

## Offsets: Tracking Position

### What is an Offset?

An **offset** is a unique ID for each message within a partition.

```
Partition 0:
┌───────┬───────┬───────┬───────┬───────┬───────┐
│ Msg 0 │ Msg 1 │ Msg 2 │ Msg 3 │ Msg 4 │ Msg 5 │
└───────┴───────┴───────┴───────┴───────┴───────┘
Offset:  0       1       2       3       4       5
```

**Key Points**:
- Offsets start at 0
- Offsets increment by 1 for each new message
- Offsets are **per-partition** (not global)
- Offsets **never change** for a message

### Consumer Offsets

Consumers track which messages they've read using offsets:

```
Consumer Progress:
┌───────┬───────┬───────┬───────┬───────┬───────┐
│  Read │  Read │  Read │ Next  │       │       │
└───────┴───────┴───────┴───────┴───────┴───────┘
Offset:  0       1       2       3       4       5
                        ↑
                Current offset = 3 (next to read)
```

**Benefits**:
1. **Resume after restart**: Consumer knows where it left off
2. **Replay data**: Reset offset to re-process old data
3. **Parallel processing**: Each consumer tracks its own offset

---

## Data Flow: Producer to Consumer

### Step-by-Step Flow

```
1. Producer creates message
   ┌─────────────────┐
   │  Producer       │
   │  message = {...}│
   └────────┬────────┘
            │
2. Send to topic (with optional key)
            ▼
   ┌─────────────────┐
   │  Kafka Broker   │
   │  Topic: vehicle │
   └────────┬────────┘
            │
3. Broker assigns to partition
            ▼
   ┌─────────────────┐
   │  Partition 1    │
   │  [msg1, msg2, ...] → Append to end
   └────────┬────────┘
            │
4. Message gets offset
            ▼
   Offset 42 assigned
            │
5. Consumer reads
            ▼
   ┌─────────────────┐
   │  Consumer       │
   │  Processes msg  │
   └─────────────────┘
```

### Message Lifecycle

```
┌──────────────┐
│ Producer     │ Writes message to topic
└──────┬───────┘
       ▼
┌──────────────┐
│ Broker       │ Stores message in partition
└──────┬───────┘ Replicates to other brokers
       ▼         Serves to consumers
┌──────────────┐
│ Consumer     │ Reads and processes message
└──────┬───────┘
       ▼
┌──────────────┐
│ Retention    │ Message kept for retention period
└──────┬───────┘ (e.g., 7 days)
       ▼
┌──────────────┐
│ Deletion     │ Message auto-deleted after retention
└──────────────┘
```

**Important**: Messages are NOT deleted immediately after consumption!

---

## Replication: Fault Tolerance

### What is Replication?

**Replication** means copying each partition to multiple brokers.

```
Topic: vehicle.telemetry (3 partitions, replication factor 3)

Partition 0:
  Leader: Broker 1
  Replicas: Broker 2, Broker 3

Partition 1:
  Leader: Broker 2
  Replicas: Broker 1, Broker 3

Partition 2:
  Leader: Broker 3
  Replicas: Broker 1, Broker 2
```

### Leader and Followers

For each partition:
- **Leader**: Handles all reads and writes
- **Followers**: Replicate data from leader (backups)

```
Partition 0 Replication:

┌─────────────┐          ┌─────────────┐          ┌─────────────┐
│  Broker 1   │          │  Broker 2   │          │  Broker 3   │
│             │          │             │          │             │
│  LEADER     │  sync    │  FOLLOWER   │  sync    │  FOLLOWER   │
│  [1,2,3,4]  ├─────────→│  [1,2,3,4]  ├─────────→│  [1,2,3,4]  │
└─────────────┘          └─────────────┘          └─────────────┘
   ↑      ↓
Producers Consumers
   (write/read from leader only)
```

### What Happens When a Broker Fails?

```
Before Failure:
Broker 1 (Leader P0) | Broker 2 (Follower P0) | Broker 3 (Follower P0)
      ✅              |         ✅             |         ✅

Broker 1 Crashes:
Broker 1 (DOWN) | Broker 2 (NEW LEADER P0) | Broker 3 (Follower P0)
      ❌         |            ✅             |           ✅

After Recovery:
Broker 1 (Follower P0) | Broker 2 (Leader P0) | Broker 3 (Follower P0)
       ✅              |          ✅           |          ✅
```

**Result**: No data loss, no downtime for consumers!

### Replication Factor

**Replication Factor (RF)** = Number of copies of each partition

```
RF = 1: No replication (dangerous!)
  - Data loss if broker fails

RF = 2: One backup
  - Can survive 1 broker failure

RF = 3: Two backups (recommended for production)
  - Can survive 2 broker failures
```

**Our Lab**: RF = 1 (single broker, no replication - OK for learning)

---

## ZooKeeper: The Coordinator

### What is ZooKeeper?

**ZooKeeper** is a separate service that Kafka uses for coordination.

**Responsibilities**:
1. **Broker Management**: Track which brokers are alive
2. **Leader Election**: Choose partition leaders when brokers fail
3. **Metadata Storage**: Store topic/partition configuration
4. **Consumer Group Coordination**: Assign partitions to consumers

```
┌──────────────────────────────────────┐
│         ZooKeeper Ensemble           │
│  (Separate cluster, 3-5 servers)     │
│                                      │
│  - Stores metadata                   │
│  - Monitors broker health            │
│  - Elects partition leaders          │
└──────────┬───────────────────────────┘
           │
           ↓
┌──────────────────────────────────────┐
│          Kafka Brokers               │
│  Brokers register with ZooKeeper     │
│  Report health, receive instructions │
└──────────────────────────────────────┘
```

### The Future: KRaft Mode

**KRaft** (Kafka Raft) is replacing ZooKeeper:

**Old (Before Kafka 3.3)**:
```
ZooKeeper Cluster + Kafka Cluster = 2 systems to manage
```

**New (Kafka 3.3+)**:
```
Kafka Cluster with KRaft = 1 system to manage
```

**Benefits**:
- Simpler deployment
- Better scalability (support millions of partitions)
- Faster operations

**Our Lab**: We'll use ZooKeeper (still default in most tutorials, easier to learn)

---

## Message Retention

### How Long are Messages Kept?

Kafka retains messages for a **configurable period**, regardless of whether they've been consumed.

**Time-Based Retention** (default):
```
retention.ms = 604800000  (7 days)

Day 1: [msg1, msg2, msg3]
Day 2: [msg1, msg2, msg3, msg4, msg5]
Day 3: [msg1, msg2, msg3, msg4, msg5, msg6]
...
Day 8: [msg4, msg5, msg6, msg7, msg8]  (msg1-3 deleted)
```

**Size-Based Retention**:
```
retention.bytes = 1073741824  (1 GB per partition)

When partition exceeds 1 GB, oldest messages are deleted
```

### Why Not Delete After Consumption?

Traditional message queues delete messages after consumption:
```
RabbitMQ:
Queue: [msg1, msg2, msg3]
Consumer reads msg1 → Queue: [msg2, msg3]  (msg1 deleted)
```

Kafka keeps messages for the retention period:
```
Kafka:
Topic: [msg1, msg2, msg3]
Consumer reads msg1 → Topic: [msg1, msg2, msg3]  (still there!)
Another consumer can also read msg1!
```

**Benefits**:
- **Multiple consumers** can read the same data
- **Replay**: Re-process data by resetting offset
- **Late consumers**: New systems can process historical data

---

## Performance Characteristics

### Why is Kafka So Fast?

**1. Sequential I/O**
```
Disk Writes:
Random writes: 100-200 IOPS (slow)
Sequential writes: 1000+ MB/sec (fast!)

Kafka appends messages sequentially (fast!)
```

**2. Zero-Copy**
- Data goes directly from disk to network (bypasses CPU)
- OS-level optimization

**3. Batching**
- Producers batch multiple messages
- Reduces network overhead

**4. Compression**
- Messages can be compressed (gzip, snappy, lz4)
- Reduces network and disk usage

### Typical Performance

**Throughput**:
- Producers: 100K-1M messages/sec per broker
- Consumers: 200K-2M messages/sec per broker

**Latency**:
- End-to-end: 5-15 milliseconds (p99)
- Producer to broker: < 5 ms
- Broker to consumer: < 5 ms

**Our Lab** (single laptop):
- 20 messages/sec (vehicle telemetry)
- Good enough for learning!

---

## Key Architecture Takeaways

✅ **Brokers** are Kafka servers (multiple = cluster)

✅ **Topics** organize messages by category

✅ **Partitions** enable parallelism and ordering (within partition)

✅ **Offsets** uniquely identify messages in a partition

✅ **Replication** provides fault tolerance (leader + followers)

✅ **ZooKeeper** coordinates the cluster (being replaced by KRaft)

✅ **Messages are retained** for a period (not deleted after consumption)

✅ **Performance** is excellent due to sequential I/O, batching, and zero-copy

---

## What You'll Build in the Lab

In Module 1's lab, you'll set up:

```
┌──────────────────────────────────────┐
│         Your Laptop                  │
│                                      │
│  ┌────────────────────────────────┐  │
│  │  Docker Container: Zookeeper   │  │
│  └────────────────────────────────┘  │
│                                      │
│  ┌────────────────────────────────┐  │
│  │  Docker Container: Kafka Broker│  │
│  │  - Topics                      │  │
│  │  - Partitions                  │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
```

You'll:
1. Start Zookeeper and Kafka with Docker Compose
2. Create a topic manually
3. Send messages using console producer
4. Read messages using console consumer
5. Observe partitions and offsets

---

## Next Steps

✅ You now understand Kafka's architecture!

**Next Reading**: [03-topics-partitions-offsets.md](03-topics-partitions-offsets.md) - Deep dive into these core concepts

**Then Practice**: [../lab/README.md](../lab/README.md) - Get hands-on with Kafka!

---

## Further Reading (Optional)

- [Kafka Architecture Internals](https://kafka.apache.org/documentation/#design)
- [Confluent: Kafka Replication](https://docs.confluent.io/platform/current/kafka/replication.html)
- [Understanding ZooKeeper's Role](https://zookeeper.apache.org/doc/current/zookeeperOver.html)

---

**Ready?** Continue to [Topics, Partitions & Offsets →](03-topics-partitions-offsets.md)
